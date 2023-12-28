import logging
import requests
import yaml
from pathlib import Path
from DataMaintenance.timer import timer
from DataMaintenance.data_controller import DataController
from DataMaintenance.medical_site_data_struct import MedicalSiteDataStructure

logging.getLogger("urllib3").setLevel(logging.WARNING)


class FetchMedicalSites:
    def __init__(self):
        self.data_source_config = None
        self._read_data_source_config()
        self.db_controller = DataController()

    def _read_data_source_config(self):
        config_file = Path(__file__).parent.resolve() / "nhi_data_source_config.yaml"
        with open(config_file, 'r', encoding='utf-8') as config:
            self.data_source_config = yaml.safe_load(config)

    @staticmethod
    def _convert_raw_data(raw_data_entry):
        medical_site_data = MedicalSiteDataStructure()
        medical_site_data.insert_data(raw_data_entry)
        return medical_site_data.get_medical_site_data()

    def _request_data_with_resource_id(self, identifier_id, resource_id):
        # Fetch data count with identifiers
        iter_limit = int(self.data_source_config.get('limit'))
        data_count = 0
        data_records = list()
        id_url = f"https://{self.data_source_config.get('host')}{self.data_source_config.get('identifier_api_path')}{identifier_id}"
        response = requests.get(id_url)
        try:
            data_count = int(response.json().get("numberOfData"))
            logging.info(f"Data count from NHI is {data_count}.")
        except ValueError:
            logging.error(f"Error parsing the data count from identifier {identifier_id}.")

        # Fetch data store
        resource_url = f"https://{self.data_source_config.get('host')}{self.data_source_config.get('resource_api_path')}{resource_id}"
        # First 1~1000
        response = requests.get(resource_url)
        logging.debug(f"Fetch data range <= {iter_limit}.")
        temp_result_list = response.json().get("result").get("records")
        for temp_result in temp_result_list:
            converted_data = self._convert_raw_data(temp_result)
            if converted_data:
                data_records.append(converted_data)
        # Greedy fetch while each round returns 1000 (limit) entries.
        i = 1
        while len(temp_result_list) == iter_limit:
            fetch_params = {'offset': i * iter_limit, 'limit': iter_limit}
            logging.debug(f"Continue to fetch data from offset {i * iter_limit}")
            response = requests.get(resource_url, params=fetch_params)
            if not response.json().get("result"):
                logging.error(f"Incomplete data found in the response, stop fetching data from NHI. {response.json()}")
                break
            temp_result_list = response.json().get("result").get("records")
            for temp_result in temp_result_list:
                converted_data = self._convert_raw_data(temp_result)
                if converted_data:
                    data_records.append(converted_data)
            i += 1

        logging.info(f"Fetched total {len(data_records)} entries, compared with NHI data count {data_count}.")
        return data_records

    def _process_data_to_db(self, db_collection):
        logging.debug("Requesting data from NHI...")
        identifier_id = self.data_source_config.get("identifiers").get(db_collection)   # For fetching data count.
        resource_id = self.data_source_config.get("resources").get(db_collection)
        data_list = self._request_data_with_resource_id(identifier_id, resource_id)
        logging.debug(f"Processing new data for collection {db_collection}.")
        if self.db_controller.count_in_collection(db_collection) == 0:
            logging.debug("No data found in local database. Insert everything.")
            self.db_controller.insert_multi_to_collection(db_collection, data_list)
            logging.debug("Data secured.")
        else:
            logging.debug("Replacing old data with new ones.")
            for medical_site in data_list:
                site_id = medical_site.get("site_id")
                query = {"site_id": site_id}
                logging.debug(f"Processing {site_id}.")
                if exists := self.db_controller.count_in_collection(db_collection, query) > 0:
                    logging.debug(f"The site id {site_id} exists: {exists}.")
                    self.db_controller.replace_one_to_collection(db_collection, query, medical_site)
                else:
                    self.db_controller.insert_one_to_collection(db_collection, medical_site)

        # Create additional index
        self.db_controller.create_index_in_collection(db_collection, "site_id", unique=True)    # ID is unique.
        self.db_controller.create_index_in_collection(db_collection, "site_name")
        self.db_controller.create_index_in_collection(db_collection, "site_region_lv1")
        self.db_controller.create_index_in_collection(db_collection, ["site_region_lv1", "site_region_lv2"])
        count = self.db_controller.count_in_collection(db_collection)
        return count

    @timer
    def update_medical_centers(self):
        db_collection = "medical_center"
        processed_count = self._process_data_to_db(db_collection=db_collection)
        logging.debug(f"Data Secured. There are {processed_count} entries of medical centers.")

    @timer
    def update_regional_hospital(self):
        db_collection = "regional_hospital"
        processed_count = self._process_data_to_db(db_collection=db_collection)
        logging.debug(f"Data Secured. There are {processed_count} entries of regional hospitals.")

    @timer
    def update_district_hospital(self):
        db_collection = "district_hospital"
        processed_count = self._process_data_to_db(db_collection=db_collection)
        logging.debug(f"Data Secured. There are {processed_count} entries of district_hospitals.")

    @timer
    def update_small_clinic(self):
        db_collection = "small_clinic"
        processed_count = self._process_data_to_db(db_collection=db_collection)
        logging.debug(f"Data Secured. There are {processed_count} entries of small clinics.")

    @timer
    def update_pharmacy(self):
        db_collection = "pharmacy"
        processed_count = self._process_data_to_db(db_collection=db_collection)
        logging.debug(f"Data Secured. There are {processed_count} entries of pharmacies.")

    def update_all(self):
        self.update_medical_centers()
        self.update_regional_hospital()
        self.update_district_hospital()
        self.update_small_clinic()
        self.update_pharmacy()

import logging
import requests
import yaml
from timer import timer
from pathlib import Path
from data_controller import DataController

logging.getLogger("urllib3").setLevel(logging.WARNING)


class FetchMedicalSites:
    def __init__(self):
        self.data_source_config = None
        self._read_data_source_config()
        self.db_controller = DataController()

    def _read_data_source_config(self):
        config_file = Path("nhi_data_source_config.yaml")
        with open(config_file, 'r', encoding='utf-8') as config:
            self.data_source_config = yaml.safe_load(config)

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
        # first 1~1000
        response = requests.get(resource_url)
        logging.debug("Fetch data range <= 1000.")
        temp_result = response.json().get("result").get("records")
        data_records += temp_result
        # # continue with increasing offset
        # if data_count > iter_limit:
        #     for i in range(1, data_count // iter_limit + 1):
        #         fetch_params = {'offset': i*iter_limit}
        #         logging.debug(f"Total data count is {data_count}. Fetch data from offset {i * iter_limit}")
        #         response = requests.get(resource_url, params=fetch_params)
        #         result = response.json().get("result").get("records")
        #         data_records += result
        i = 1
        while len(temp_result) == iter_limit:     # Greedy fetch while each round returns 1000 (limit) entries.
            fetch_params = {'offset': i * iter_limit}
            logging.debug(f"Continue to fetch data from offset {i * iter_limit}")
            response = requests.get(resource_url, params=fetch_params)
            temp_result = response.json().get("result").get("records")
            data_records += temp_result
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
                site_name = medical_site.get("Hosp_Name")
                query = {"Hosp_Name": site_name}
                logging.debug(f"Processing {site_name}.")
                if self.db_controller.count_in_collection(db_collection, query) > 0:
                    self.db_controller.replace_one_to_collection(db_collection, query, medical_site)
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

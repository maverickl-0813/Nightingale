import yaml
from pathlib import Path


class MedicalSiteDataBase:
    def __init__(self):
        self.data_source_config = dict()
        self._read_data_source_config()
        self.base_structure = {
            "site_id": {"field_mapping": self.data_source_config["fields"][0], "value": ""},
            "site_name": {"field_mapping": self.data_source_config["fields"][1], "value": ""},
            "site_type": {"field_mapping": self.data_source_config["fields"][6], "value": ""},
            "site_telephone": {"field_mapping": self.data_source_config["fields"][3], "value": ""},
            "site_address": {"field_mapping": self.data_source_config["fields"][4], "value": ""},
            "site_service_list": {"field_mapping": self.data_source_config["fields"][7], "values": list()},
            "site_function_list": {"field_mapping": self.data_source_config["fields"][8], "values": list()},
            "site_working_hours": {"field_mapping": self.data_source_config["fields"][10], "values": list()},
            "site_remark": {"field_mapping": self.data_source_config["fields"][11], "value": ""}
        }

    def _read_data_source_config(self):
        config_file = Path("nhi_data_source_config.yaml")
        with open(config_file, 'r', encoding='utf-8') as config:
            self.data_source_config = yaml.safe_load(config)

    def insert_data(self, data_dict):
        for key in self.base_structure.keys():
            # process list from concatenated string value.
            if isinstance(self.base_structure.get(key).get("values"), list):
                splitter = None
                if "," in data_dict[self.base_structure[key]['field_mapping']]:
                    splitter = ','
                elif '、' in data_dict[self.base_structure[key]['field_mapping']]:
                    splitter = '、'
                self.base_structure[key]['values'] = data_dict[self.base_structure[key]['field_mapping']].strip().split(splitter)
            else:
                self.base_structure[key]['value'] = data_dict[self.base_structure[key]['field_mapping']].strip()

    def get_medical_site_data(self):
        return self.base_structure

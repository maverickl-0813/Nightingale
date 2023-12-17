# -*- coding: utf-8 -*-
import logging
import yaml
from pathlib import Path


class MedicalSiteDataStructure:
    def __init__(self):
        self.base_structure = dict()
        self.data_mapping = dict()
        self._read_data_structure_and_mapping()

    def _read_data_structure_and_mapping(self):
        data_structure_file = Path("medical_site_data_struct.yaml")
        with open(data_structure_file, 'r', encoding='utf-8') as ds:
            read_data = yaml.safe_load(ds)
            self.base_structure = read_data['fields']
            self.data_mapping = read_data['field_mapping']

    def _process_working_hours(self, raw_data):
        zh_day_name_mappings = {"星期一": "Monday",
                                "星期二": "Tuesday",
                                "星期三": "Wednesday",
                                "星期四": "Thursday",
                                "星期五": "Friday",
                                "星期六": "Saturday",
                                "星期日": "Sunday"}
        am_pm_mappings = {"上午": "morning", "下午": "afternoon", "晚上": "evening"}
        open_mappings = {"看診": 'Y', "休診": 'N'}

        raw_list = raw_data.strip().split('、')
        for opening in raw_list:
            zh_day = opening[:3]
            am_pm = opening[3:5]
            work = opening[-2:]
            self.base_structure.get("site_working_hours")[zh_day_name_mappings.get(zh_day)][am_pm_mappings.get(am_pm)] = open_mappings.get(work)

    def insert_data(self, data_dict):
        for key in self.base_structure.keys():
            if isinstance(self.base_structure.get(key), list):
                splitter = None
                if "," in data_dict[self.data_mapping.get(key)]:
                    splitter = ','
                self.base_structure[key] = data_dict[self.data_mapping.get(key)].strip().split(splitter)
            elif isinstance(self.base_structure.get(key), dict):
                if key == "site_working_hours" and data_dict.get(self.data_mapping.get(key)):
                    self._process_working_hours(data_dict[self.data_mapping.get(key)])
            else:
                self.base_structure[key] = data_dict[self.data_mapping.get(key)].strip()

    def get_medical_site_data(self):
        return self.base_structure

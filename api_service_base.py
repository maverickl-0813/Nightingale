# -*- coding: utf-8 -*-
from bson import json_util
import json
from flask_restful import Resource
from DataMaintenanceProcess.data_controller import DataController
import taiwan_division_list


class BaseClass(Resource):
    def __init__(self):
        self.db_controller = DataController()
        self.supported_medical_site = list()
        self.tw_division_list = taiwan_division_list.area_data
        self.tw_lv1_list = self.tw_division_list.keys()

    @staticmethod
    def _convert_mongodb_output_to_json(data):
        return json.loads(json.dumps(data, default=json_util.default))

    @staticmethod
    def _return_error_status(status_code, message):
        return {'status': "error", 'error': {'code': int(status_code), 'message': message}}, int(status_code)

    @staticmethod
    def _return_success_status(data):
        if data:
            return {'status': "success", 'data': data}, 200
        else:
            return {'status': "success"}, 200

    @staticmethod
    def _is_required_args_exists(arg_list):
        for arg in arg_list:
            if not arg:
                return False
        return True

    def _is_site_type_valid(self, site_type):
        if site_type not in self.supported_medical_site:
            return False
        return True

    def _site_division_preprocess(self, site_division):
        if len(site_division) > 3:    # has 2 levels
            division_lv1 = site_division[:3]
            division_lv2 = site_division[3:]
            if division_lv1 in self.tw_lv1_list and division_lv2 in self.tw_division_list[division_lv1]:
                return division_lv1, division_lv2
        elif site_division in self.tw_lv1_list:     # only has 1 level
            return site_division, ''
        return None

    @staticmethod
    def _replace_tai(text):
        text = text.replace("台", "臺")
        return text

    def _list_sites_by_type(self, site_type):
        results = list()
        query_results_bson = self.db_controller.query_multi_in_collection(resource=site_type)
        for item in query_results_bson:
            item = self._convert_mongodb_output_to_json(item)
            results.append(item)
        return results

    def _query_site_by_id(self, site_type, site_id, return_detail=True):
        query_result = None
        query_projection = dict()
        if not return_detail:
            query_projection = {"site_region_lv1": 0,
                                "site_region_lv2": 0,
                                "site_service_list": 0,
                                "site_function_list": 0,
                                "site_working_hours": 0}
        if site_id:
            query_filter = {'site_id': site_id}
            query_result_bson = self.db_controller.query_one_in_collection(resource=site_type,
                                                                           query_filter=query_filter,
                                                                           query_projection=query_projection)
            query_result = self._convert_mongodb_output_to_json(query_result_bson)
        return query_result

    def _query_site_list_by_division(self, site_type, site_division):
        results = list()
        query_filter = dict()
        site_division = self._replace_tai(site_division)

        if site_division:
            if (dv_tuple := self._site_division_preprocess(site_division)) is not None:
                query_filter['site_region_lv1'] = dv_tuple[0]
                if dv_tuple[1]:
                    query_filter['site_region_lv2'] = dv_tuple[1]
            else:  # Invalid site division input, return empty results immediately.
                return results

        # query database
        query_result_bson = self.db_controller.query_multi_in_collection(resource=site_type, query_filter=query_filter)
        for item in query_result_bson:
            item = self._convert_mongodb_output_to_json(item)
            results.append(item)
        return results

    def _count_site_by_type(self, site_type):
        count = self.db_controller.count_in_collection(resource=site_type)
        return count

    def _count_site_by_division(self, site_type, site_division):
        query_filter = dict()
        site_division = self._replace_tai(site_division)

        if site_division:
            if (dv_tuple := self._site_division_preprocess(site_division)) is not None:
                query_filter['site_region_lv1'] = dv_tuple[0]
                if dv_tuple[1]:
                    query_filter['site_region_lv2'] = dv_tuple[1]
            else:   # Invalid site division input, return 0 immediately.
                return 0

        # query database
        count = self.db_controller.count_in_collection(resource=site_type, query_filter=query_filter)
        return count

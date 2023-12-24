# -*- coding: utf-8 -*-
from bson import json_util
import json
from flask_restful import Resource
from DataMaintenanceProcess.data_controller import DataController


class BaseClass(Resource):
    def __init__(self):
        self.db_controller = DataController()
        self.supported_medical_site = list()

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

    @staticmethod
    def _replace_tai(text):
        text = text.replace("台", "臺")
        return text

    def _list_sites_by_type(self, site_type):
        results = list()
        query_results_bson = self.db_controller.query_multi_in_collection(resource=site_type)
        for item in query_results_bson:
            item = self._convert_mongodb_output_to_json(item)
            del item["_id"]
            results.append(item)
        return results

    def _query_site_type_by_id(self, site_type, site_id):
        query_result = None
        if site_id:
            query_filter = {'site_id': site_id}
            query_result_bson = self.db_controller.query_one_in_collection(resource=site_type, query_filter=query_filter)
            query_result = self._convert_mongodb_output_to_json(query_result_bson)
            del query_result["_id"]
        return query_result

    def _query_site_list_by_division(self, site_type, site_division):
        results = list()
        site_division = self._replace_tai(site_division)
        if site_division:
            if len(site_division) > 3:
                division_lv1 = site_division[:3]
                division_lv2 = site_division[3:]
                query_filter = {'site_region_lv1': division_lv1, 'site_region_lv2': division_lv2}
            else:
                query_filter = {'site_region_lv1': site_division}
            query_result_bson = self.db_controller.query_multi_in_collection(resource=site_type, query_filter=query_filter)
            for item in query_result_bson:
                item = self._convert_mongodb_output_to_json(item)
                del item["_id"]
                results.append(item)
        return results

    def _count_site_by_type(self, site_type):
        count = self.db_controller.count_in_collection(resource=site_type)
        return count

    def _count_site_by_division(self, site_type, site_division):
        count = 0
        site_division = self._replace_tai(site_division)
        if site_division:
            if len(site_division) > 3:
                division_lv1 = site_division[:3]
                division_lv2 = site_division[3:]
                query_filter = {'site_region_lv1': division_lv1, 'site_region_lv2': division_lv2}
            else:
                query_filter = {'site_region_lv1': site_division}
            count = self.db_controller.count_in_collection(resource=site_type, query_filter=query_filter)
        return count

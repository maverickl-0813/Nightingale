from bson import json_util
import json
from flask import request
from flask_restful import Resource
from DataMaintenanceProcess.data_controller import DataController


supported_medical_site = ["medical_center", "regional_hospital", "district_hospital"]


class BaseClass(Resource):
    def __init__(self):
        self.db_controller = DataController()

    @staticmethod
    def _convert_mongodb_output_to_json(data):
        return json.loads(json.dumps(data, default=json_util.default))

    @staticmethod
    def _validate_site_type(site_type):
        if site_type not in supported_medical_site:
            return {'message': f"Not supported medical site type: {site_type}"}, 400

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


class GetSiteBasicData(BaseClass):
    def __init__(self):
        super().__init__()

    def get(self):
        site_type = request.args.get("type")
        site_id = request.args.get("id")
        self._validate_site_type(site_type)
        query_result = self._query_site_type_by_id(site_type=site_type, site_id=site_id)
        for key in ["site_region_lv1", "site_region_lv2", "site_service_list", "site_function_list",
                    "site_working_hours"]:
            del query_result[key]
        return {'message': 'success', 'data': query_result}, 200


class GetSiteWorkingHours(BaseClass):
    def __init__(self):
        super().__init__()

    def get(self):
        site_type = request.args.get("type")
        site_id = request.args.get("id")
        self._validate_site_type(site_type)
        query_result = self._query_site_type_by_id(site_type=site_type, site_id=site_id)
        result = query_result.pop("site_working_hours")
        return {'message': 'success', 'data': result}, 200


class GetMedicalSiteList(BaseClass):
    def __init__(self):
        super().__init__()

    def get(self):
        site_type = request.args.get("type")
        self._validate_site_type(site_type)
        query_result = self._list_sites_by_type(site_type=site_type)
        site_count = self._count_site_by_type(site_type=site_type)
        return {'message': 'success', 'count': site_count, 'data': query_result}, 200


class GetSiteCountByType(BaseClass):
    def __init__(self):
        super().__init__()

    def get(self):
        site_type = request.args.get("type")
        self._validate_site_type(site_type)
        site_count = self._count_site_by_type(site_type=site_type)
        return {'message': 'success', 'count': site_count}, 200


class GetSiteListByDivision(BaseClass):

    def __init__(self):
        super().__init__()

    def get(self):
        site_type = request.args.get("type")
        site_division = request.args.get("division")
        self._validate_site_type(site_type)
        query_result = self._query_site_list_by_division(site_type=site_type, site_division=site_division)
        count = len(query_result)
        return {'message': 'success', 'count': count, 'data': query_result}

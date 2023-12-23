from flask import request
from api_service_base import BaseClass


supported_medical_site = ["medical_center", "regional_hospital", "district_hospital"]


class GetSiteBasicData(BaseClass):
    def __init__(self):
        self.supported_medical_site = supported_medical_site
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
        self.supported_medical_site = supported_medical_site
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
        self.supported_medical_site = supported_medical_site
        super().__init__()

    def get(self):
        site_type = request.args.get("type")
        self._validate_site_type(site_type)
        query_result = self._list_sites_by_type(site_type=site_type)
        site_count = self._count_site_by_type(site_type=site_type)
        return {'message': 'success', 'count': site_count, 'data': query_result}, 200


class GetSiteCountByType(BaseClass):
    def __init__(self):
        self.supported_medical_site = supported_medical_site
        super().__init__()

    def get(self):
        site_type = request.args.get("type")
        self._validate_site_type(site_type)
        site_count = self._count_site_by_type(site_type=site_type)
        return {'message': 'success', 'count': site_count}, 200


class GetSiteListByDivision(BaseClass):

    def __init__(self):
        self.supported_medical_site = supported_medical_site
        super().__init__()

    def get(self):
        site_type = request.args.get("type")
        site_division = request.args.get("division")
        self._validate_site_type(site_type)
        query_result = self._query_site_list_by_division(site_type=site_type, site_division=site_division)
        count = len(query_result)
        return {'message': 'success', 'count': count, 'data': query_result}

from flask import request
from api_service_base import BaseClass


supported_medical_site = ["medical_center", "regional_hospital", "district_hospital", "small_clinic"]


class GetSiteBasicData(BaseClass):
    def __init__(self):
        super().__init__()
        self.supported_medical_site = supported_medical_site

    def get(self):
        site_type = request.args.get("type")
        site_id = request.args.get("id")

        if not self._is_required_args_exists([site_type, site_id]):
            return self._return_error_status(status_code=400, message=f"Query string incomplete.")

        if not self._is_site_type_valid(site_type):
            return self._return_error_status(status_code=400, message=f"Not supported medical site type: {site_type}")

        query_result = self._query_site_type_by_id(site_type=site_type, site_id=site_id)
        for key in ["site_region_lv1", "site_region_lv2", "site_service_list", "site_function_list",
                    "site_working_hours"]:
            del query_result[key]
        return self._return_success_status(data=query_result)


class GetSiteWorkingHours(BaseClass):
    def __init__(self):
        super().__init__()
        self.supported_medical_site = supported_medical_site

    def get(self):
        site_type = request.args.get("type")
        site_id = request.args.get("id")

        if not self._is_required_args_exists([site_type, site_id]):
            return self._return_error_status(status_code=400, message=f"Query string incomplete.")

        if not self._is_site_type_valid(site_type):
            return self._return_error_status(status_code=400, message=f"Not supported medical site type: {site_type}")

        query_result = self._query_site_type_by_id(site_type=site_type, site_id=site_id)
        result = query_result.pop("site_working_hours")
        return self._return_success_status(data=result)


class GetMedicalSiteList(BaseClass):
    def __init__(self):
        super().__init__()
        self.supported_medical_site = supported_medical_site

    def get(self):
        site_type = request.args.get("type")

        if not self._is_required_args_exists([site_type]):
            return self._return_error_status(status_code=400, message=f"Query string incomplete.")

        if not self._is_site_type_valid(site_type):
            return self._return_error_status(status_code=400, message=f"Not supported medical site type: {site_type}")

        query_result = self._list_sites_by_type(site_type=site_type)
        site_count = self._count_site_by_type(site_type=site_type)
        result = {'total_count': site_count, 'items': query_result}
        return self._return_success_status(data=result)


class GetSiteCountByType(BaseClass):
    def __init__(self):
        super().__init__()
        self.supported_medical_site = supported_medical_site

    def get(self):
        site_type = request.args.get("type")

        if not self._is_required_args_exists([site_type]):
            return self._return_error_status(status_code=400, message=f"Query string incomplete.")

        if not self._is_site_type_valid(site_type):
            return self._return_error_status(status_code=400, message=f"Not supported medical site type: {site_type}")

        site_count = self._count_site_by_type(site_type=site_type)
        result = {'total_count': site_count}
        return self._return_success_status(data=result)


class GetSiteListByDivision(BaseClass):

    def __init__(self):
        super().__init__()
        self.supported_medical_site = supported_medical_site

    def get(self):
        site_type = request.args.get("type")
        site_division = request.args.get("division")

        if not self._is_required_args_exists([site_type, site_division]):
            return self._return_error_status(status_code=400, message=f"Query string incomplete.")

        if not self._is_site_type_valid(site_type):
            return self._return_error_status(status_code=400, message=f"Not supported medical site type: {site_type}")

        query_result = self._query_site_list_by_division(site_type=site_type, site_division=site_division)
        count = len(query_result)
        result = {'total_count': count, 'items': query_result}
        return self._return_success_status(data=result)


class GetSiteCountByDivision(BaseClass):

    def __init__(self):
        super().__init__()
        self.supported_medical_site = supported_medical_site

    def get(self):
        site_type = request.args.get("type")
        site_division = request.args.get("division")

        if not self._is_required_args_exists([site_type, site_division]):
            return self._return_error_status(status_code=400, message=f"Query string incomplete.")

        if not self._is_site_type_valid(site_type):
            return self._return_error_status(status_code=400, message=f"Not supported medical site type: {site_type}")

        site_count = self._count_site_by_division(site_type=site_type, site_division=site_division)
        result = {'total_count': site_count}
        return self._return_success_status(data=result)

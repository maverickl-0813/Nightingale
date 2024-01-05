from flask import request
from api_service_base import BaseClass


supported_facility_type = ["medical_center", "regional_hospital", "district_hospital", "small_clinic"]


class GetSiteBasicData(BaseClass):
    def __init__(self):
        super().__init__()
        self.supported_facility_type = supported_facility_type

    def get(self, site_id):

        if not self._is_required_args_exists([site_id]):
            return self._return_error_status(status_code=400,
                                             message=f"Query string incomplete.")
        for site_type in self.supported_facility_type:
            query_result = self._query_site_by_id(site_type=site_type, site_id=site_id, return_detail=False)
            if query_result:
                return self._return_success_status(data=query_result)

        # Not found.
        return self._return_error_status(status_code=404, message=f"Facility not found. (id: {site_id})")


class GetSiteWorkingHours(BaseClass):
    def __init__(self):
        super().__init__()
        self.supported_facility_type = supported_facility_type

    def get(self, site_id):
        if not self._is_required_args_exists([site_id]):
            return self._return_error_status(status_code=400,
                                             message=f"Query string incomplete.")

        for site_type in self.supported_facility_type:
            query_result = self._query_site_by_id(site_type=site_type, site_id=site_id, return_detail=True)
            if query_result:
                result = query_result.pop("site_working_hours")
                return self._return_success_status(data=result)

        # Not found.
        return self._return_error_status(status_code=404, message=f"Facility not found. (id: {site_id})")


class GetMedicalSiteList(BaseClass):
    def __init__(self):
        super().__init__()
        self.supported_facility_type = supported_facility_type

    def get(self, site_type):

        # Filter with division.
        site_division = request.args.get("division")

        if not self._is_required_args_exists([site_type]):
            return self._return_error_status(status_code=400,
                                             message=f"Query string incomplete.")

        if not self._is_site_type_valid(site_type):
            return self._return_error_status(status_code=400,
                                             message=f"Not supported medical site type: {site_type}")

        if site_division:
            query_result = self._query_site_list_by_division(site_type=site_type, site_division=site_division)
            site_count = len(query_result)
        else:
            query_result = self._list_sites_by_type(site_type=site_type)
            site_count = self._count_site_by_type(site_type=site_type)
        result = {'total_count': site_count, 'items': query_result}
        return self._return_success_status(data=result)


class GetSiteCountByType(BaseClass):
    def __init__(self):
        super().__init__()
        self.supported_facility_type = supported_facility_type

    def get(self, site_type):

        # Filter with division.
        site_division = request.args.get("division")

        if not self._is_required_args_exists([site_type]):
            return self._return_error_status(status_code=400,
                                             message=f"Query string incomplete.")

        if not self._is_site_type_valid(site_type):
            return self._return_error_status(status_code=400,
                                             message=f"Not supported medical site type: {site_type}")

        if site_division:
            site_count = self._count_site_by_division(site_type=site_type, site_division=site_division)
        else:
            site_count = self._count_site_by_type(site_type=site_type)
        result = {'total_count': site_count}
        return self._return_success_status(data=result)

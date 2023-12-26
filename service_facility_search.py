from flask import request
from api_service_base import BaseClass

supported_medical_site = ["medical_center", "regional_hospital", "district_hospital", "small_clinic"]


class SearchSites(BaseClass):

    def __init__(self):
        super().__init__()
        self.supported_medical_site = supported_medical_site

    def _query_site_list_by_division_and_function_list(self, site_type, site_division, site_function_list):
        results = list()
        query_filter = dict()
        site_division = self._replace_tai(site_division)

        if site_division:
            if (dv_tuple := self._site_division_preprocess(site_division)) is not None:
                query_filter['site_region_lv1'] = dv_tuple[0]
                if dv_tuple[1]:
                    query_filter['site_region_lv2'] = dv_tuple[1]
            else:   # Invalid site division input, return empty results immediately.
                return results

        if site_function_list:
            query_filter['site_function_list'] = {'$all': site_function_list}

        # query database
        query_results_bson = self.db_controller.query_multi_in_collection(resource=site_type, query_filter=query_filter)
        for item in query_results_bson:
            item = self._convert_mongodb_output_to_json(item)
            del item["_id"]
            results.append(item)
        return results

    def post(self):
        request_data = request.json  # Get JSON data from the request body

        site_type_list = request_data.get("type") if request_data.get("type") else None
        site_division = request_data.get("division") if request_data.get("division") else None
        site_function_list = request_data.get("function") if request_data.get("function") else None

        if not self._is_required_args_exists([site_type_list, site_division, site_function_list]):
            return self._return_error_status(status_code=400,
                                             message=f"Query criteria incomplete.")

        for site_type in site_type_list:
            if not self._is_site_type_valid(site_type):
                return self._return_error_status(status_code=400,
                                                 message=f"Not supported medical site type: {site_type}")

        if len(site_function_list) == 1 and site_function_list[0] == '':
            return self._return_error_status(status_code=400,
                                             message=f"Function is not provided with \"function\" argument properly.")

        query_result = list()
        for site_type in site_type_list:
            query_type_result = self._query_site_list_by_division_and_function_list(site_type=site_type,
                                                                                    site_division=site_division,
                                                                                    site_function_list=site_function_list)
            query_result += query_type_result

        count = len(query_result)
        result = {'total_count': count, 'items': query_result}
        return self._return_success_status(data=result)

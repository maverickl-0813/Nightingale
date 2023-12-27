from flask import request
from api_service_base import BaseClass

supported_medical_site = ["medical_center", "regional_hospital", "district_hospital", "small_clinic"]


class SearchSites(BaseClass):

    def __init__(self):
        super().__init__()
        self.supported_medical_site = supported_medical_site

    def _query_sites(self, site_type, site_division, site_function_list, site_name_kw):
        results = list()
        query_filter = dict()

        if site_division:
            site_division = self._replace_tai(site_division)
            if (dv_tuple := self._site_division_preprocess(site_division)) is not None:
                query_filter['site_region_lv1'] = dv_tuple[0]
                if dv_tuple[1]:
                    query_filter['site_region_lv2'] = dv_tuple[1]
            else:   # Invalid site division input, return empty results immediately.
                return results

        if site_function_list:
            query_filter['site_function_list'] = {'$all': site_function_list}

        if site_name_kw:
            query_filter['site_name'] = {'$regex': site_name_kw}

        # query database
        query_results_bson = self.db_controller.query_multi_in_collection(resource=site_type, query_filter=query_filter)
        for item in query_results_bson:
            item = self._convert_mongodb_output_to_json(item)
            del item["_id"]
            results.append(item)
        return results

    def post(self):
        request_data = request.json if request.json else {}  # Get JSON data from the request body

        site_type_list = request_data.get("type")
        site_division = request_data.get("division")
        site_function_list = request_data.get("function")
        site_name_keyword = request_data.get("keyword")

        if not self._is_required_args_exists([site_type_list]):     # Only site type ("type") is mandatory.
            return self._return_error_status(status_code=400,
                                             message=f"Query criteria incomplete, provide 'type' with array. "
                                                     f"Supported facility types: {self.supported_medical_site}")

        for site_type in site_type_list:
            if not self._is_site_type_valid(site_type):
                return self._return_error_status(status_code=400,
                                                 message=f"Not supported medical site type: {site_type}")

        query_result = list()
        for site_type in site_type_list:
            query_type_result = self._query_sites(site_type=site_type,
                                                  site_division=site_division,
                                                  site_function_list=site_function_list,
                                                  site_name_kw=site_name_keyword)
            query_result += query_type_result

        count = len(query_result)
        result = {'total_count': count, 'items': query_result}
        return self._return_success_status(data=result)

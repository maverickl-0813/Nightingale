from flask import Flask
from flask_restful import Api
from service_facility_by_type import GetSiteBasicData
from service_facility_by_type import GetSiteCountByType
from service_facility_by_type import GetMedicalSiteList
from service_facility_by_type import GetSiteWorkingHours
from service_facility_by_type import GetSiteListByDivision
from service_facility_by_type import GetSiteCountByDivision
from service_facility_by_type import GetSiteListByDivisionAndFunction


app = Flask(__name__)
api = Api(app)

endpoints = {
    "/site_basic_data": GetSiteBasicData,
    "/site_count": GetSiteCountByType,
    "/list_sites": GetMedicalSiteList,
    "/working_hours": GetSiteWorkingHours,
    "/list_sites_by_division": GetSiteListByDivision,
    "/site_count_by_division": GetSiteCountByDivision,
    "/search_function_with_division": GetSiteListByDivisionAndFunction
}


if __name__ == '__main__':
    for endpoint, func in endpoints.items():
        api.add_resource(func, endpoint)

    app.run(host='0.0.0.0', port=6400, ssl_context="adhoc", debug=True)

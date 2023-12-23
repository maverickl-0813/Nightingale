from flask import Flask
from flask_restful import Api
from service_facility_by_type import GetSiteBasicData
from service_facility_by_type import GetSiteCountByType
from service_facility_by_type import GetMedicalSiteList
from service_facility_by_type import GetSiteWorkingHours
from service_facility_by_type import GetSiteListByDivision


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(GetSiteBasicData, "/site_basic_data")
    api.add_resource(GetSiteCountByType, "/site_count")
    api.add_resource(GetMedicalSiteList, "/list_sites")
    api.add_resource(GetSiteWorkingHours, "/working_hours")
    api.add_resource(GetSiteListByDivision, "/search_site_by_division")
    app.run(host='0.0.0.0', port=6400, ssl_context="adhoc", debug=True)

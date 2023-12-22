from flask import Flask
from flask_restful import Api
from medical_site_data_service import GetSiteBasicData
from medical_site_data_service import GetSiteCountByType
from medical_site_data_service import ListMedicalSite
from medical_site_data_service import GetSiteWorkingHours


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(GetSiteBasicData, "/site_basic_data")
    api.add_resource(GetSiteCountByType, "/site_count")
    api.add_resource(ListMedicalSite, "/list_sites")
    api.add_resource(GetSiteWorkingHours, "/working_hours")
    app.run(host='0.0.0.0', port=6400, ssl_context="adhoc", debug=True)

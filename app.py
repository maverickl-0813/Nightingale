import json
from flask import Flask, jsonify
from flask_restful import Api
from service_facility_by_type import GetSiteBasicData
from service_facility_by_type import GetSiteCountByType
from service_facility_by_type import GetMedicalSiteList
from service_facility_by_type import GetSiteWorkingHours
from service_facility_by_type import GetSiteListByDivision
from service_facility_by_type import GetSiteCountByDivision
from service_facility_search import SearchSites


app = Flask(__name__)
api = Api(app)

endpoints = {
    "/med_facility/basic_info": GetSiteBasicData,
    "/med_facility/count": GetSiteCountByType,
    "/med_facility/list": GetMedicalSiteList,
    "/med_facility/working_hours": GetSiteWorkingHours,
    "/med_facility/list_by_division": GetSiteListByDivision,
    "/med_facility/count_by_division": GetSiteCountByDivision,
    "/med_facility/search": SearchSites
}


@app.route('/nightingale-openapi.json')
def swagger():
    with open('nightingale-openapi.json', 'r') as f:
        response = jsonify(json.load(f))
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response


if __name__ == '__main__':
    for endpoint, func in endpoints.items():
        api.add_resource(func, endpoint)

    app.run(host='0.0.0.0', port=6400, ssl_context="adhoc")
    # app.run(host='0.0.0.0', port=6400)

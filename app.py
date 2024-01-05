import json
from flask import Flask, jsonify
from flask_restful import Api
from service_facility_by_type import GetSiteBasicData
from service_facility_by_type import GetSiteCountByType
from service_facility_by_type import GetMedicalSiteList
from service_facility_by_type import GetSiteWorkingHours
from service_facility_search import SearchSites


app = Flask(__name__)
api = Api(app)

endpoints = {
    "/v1/facilities/<string:site_id>": GetSiteBasicData,
    "/v1/facilities/<string:site_id>/working_hours": GetSiteWorkingHours,
    "/v1/facilities/<string:site_type>/count": GetSiteCountByType,
    "/v1/facilities/<string:site_type>/list": GetMedicalSiteList,
    "/v1/facilities/search": SearchSites
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

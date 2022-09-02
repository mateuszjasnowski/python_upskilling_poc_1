"""Endpoint for api"""
from flask import request

from app_data import app
from app_data.get_city_data import CityData


@app.route("/", methods=["GET"])
@app.route("/version", methods=["GET"])
def get_version():
    """Returns api and feeds version"""
    return {"version": "0.0.1"}


@app.route("/cities/create_city", methods=["POST"])
def cities_create_city():
    """
    Checking if city exist TODO
    Downloading data
    Uploading data to DB
    """
    request_data = request.headers
    city_name = request_data.get("city_name")
    city_url = request_data.get("city_url")

    if request_data.get("download_mode"):
        download_mode = request_data.get("download_mode")
    else:
        download_mode = True

    city_data = CityData(
        city_name=city_name, city_url=city_url, download_mode=download_mode
    )
    if city_data.return_code != 201:
        return {"Status": "Failed", "Errors": city_data.errors}, city_data.return_code

    return {"Status": "Success", "content": city_data.items()}, 201

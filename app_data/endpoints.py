"""Endpoint for api"""
from datetime import datetime

from flask import request
from sqlalchemy import exc

from app_data import app, db
from app_data.get_city_data import CityData
import app_data.city


@app.route("/", methods=["GET"])
@app.route("/version", methods=["GET"])
def get_version():
    """Returns api and feeds version"""
    return {"version": "0.0.1"}


@app.route("/cities/create_city", methods=["POST"])
def cities_create_city():
    """
    Checking if city exist
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

    print(f'ACTION: Getting city data for {city_name}')
    city_data = CityData(
        city_name=city_name, city_url=city_url, download_mode=download_mode
    )
    if city_data.return_code != 201:
        return {"Status": "Failed", "Errors": city_data.errors}, city_data.return_code

    print(f'ACTION: Checking if city {city_name} was already created')
    db_city = app_data.city.City.query.filter_by(city_name=city_name).first()
    if db_city:
        #city_id = db_city.city_id
        return {"Status": "Failed", "Error": f"City with name {city_name} already exists"}, 409
    else:
        new_city = app_data.city.City(
            city_name=city_name,
            feed_publisher_name=city_data.feed_info[0]["feed_publisher_name"],
            feed_publisher_url=city_data.feed_info[0]["feed_publisher_url"],
            feed_lang=city_data.feed_info[0]["feed_lang"],
            feed_start_date=datetime.strptime(
                city_data.feed_info[0]["feed_start_date"], "%Y%m%d"
            ),
            feed_end_date=datetime.strptime(
                city_data.feed_info[0]["feed_end_date"], "%Y%m%d"
            ),
        )
        try:
            db.session.add(new_city)
            db.session.commit()
        except exc.IntegrityError as ie:
            db.session.rollback()
            if ie.orig and len(str(ie.orig).split("\n")) > 1:
                print(str(ie.orig).split("\n")[1])
        else:
            print(f"ACTION: Added city {city_name}")
            city_id = (
                app_data.city.City.query.filter_by(city_name=city_name).first().city_id
            )

    print(f"INFO: City {city_name} with id {city_id}")

    # inset to db
    if city_data.insert_to_db(city_id):
        return {"Status": "Success", "content": city_data.items()}, 201
    return {"Status": "FAILED", "content": "Something came wrong!" }, 500

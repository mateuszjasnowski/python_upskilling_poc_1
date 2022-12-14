# pylint: disable=E1101
"""Endpoint for api"""
from datetime import datetime

from flask import request
from sqlalchemy import exc
from app_data.find_route import FindRoute

from app_data.secrets import API_VERSION
from app_data import app, db
from app_data.get_city_data import CityData
from app_data.city import City, Route
import app_data.city as city_class

from app_data.geo_point import location_to_cords, GeoPoint


@app.route("/", methods=["GET"])
@app.route("/version", methods=["GET"])
def get_version():
    """Returns api and feeds version"""
    return {"version": API_VERSION}


@app.route("/city", methods=["GET"])
def get_city():
    """
    API ENDPOINT
    Reciving:
    - city_id*
    - city_name*
    *not required

    Returning:
    {"cities": [{"city_id": id, "city_name": name},{...}]} #if multiple cities
    or
    {"city": {{"city_id": id, "city_name": name}}}
    """
    error = ""
    error_val = ""

    if "city_id" in request.args:
        get_city_id = request.args.get("city_id")
        db_get_city = City.query.filter_by(city_id=get_city_id).first()
        error = "id"
        error_val = get_city_id

    elif "city_name" in request.args:
        get_city_name = request.args.get("city_name")
        db_get_city = City.query.filter_by(city_name=get_city_name).first()
        error = "name"
        error_val = get_city_name

    else:
        db_get_city = City.query.all()

    if not db_get_city:
        return {
            "Status": "Failed",
            "Error": f"Not found any city {error} = {error_val}",
        }, 404

    if isinstance(db_get_city, list):
        return {
            "cities": [
                {"city_id": city.city_id, "city_name": city.city_name}
                for city in db_get_city
            ]
        }
    return {
        "city": {"city_id": db_get_city.city_id, "city_name": db_get_city.city_name}
    }


@app.route("/city", methods=["POST"])
def post_city_create():
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

    print(f"ACTION: Getting city data for {city_name}")
    city_data = CityData(
        city_name=city_name, city_url=city_url, download_mode=download_mode
    )
    if city_data.return_code != 201:
        return {"Status": "Failed", "Errors": city_data.errors}, city_data.return_code

    print(f"ACTION: Checking if city {city_name} was already created")
    db_city = City.query.filter_by(city_name=city_name).first()
    if db_city:
        # city_id = db_city.city_id
        return {
            "Status": "Failed",
            "Error": f"City with name {city_name} already exists",
        }, 409
    # else:
    new_city = City(
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
    except exc.IntegrityError as integrity_error:
        db.session.rollback()
        if integrity_error.orig and len(str(integrity_error.orig).split("\n")) > 1:
            print(str(integrity_error.orig).split("\n")[1])
    else:
        print(f"ACTION: Added city {city_name}")
        city_id = City.query.filter_by(city_name=city_name).first().city_id

    print(f"INFO: City {city_name} with id {city_id}")

    # inset to db
    if city_data.insert_to_db(city_id):
        return {"Status": "Success", "content": city_data.items()}, 201
    return {"Status": "FAILED", "content": "Something came wrong!"}, 500


@app.route("/city", methods=["DELETE"])  # NOT TESTED
def delete_city_delete():
    """
    API ENDPOINT
    Reciving:
    - city_id**
    - city_name**
    ** required one of

    Returning:
    TODO
    """
    error = ""
    error_val = ""
    request_data = request.headers

    if "city_id" in request_data:
        get_city_id = request_data.get("city_id")
        db_get_city = City.query.filter_by(city_id=get_city_id).first()
        error = "id"
        error_val = get_city_id
        # city_id = get_city_id

    elif "city_name" in request_data:
        get_city_name = request_data.get("city_name")
        db_get_city = City.query.filter_by(city_name=get_city_name).first()
        error = "name"
        error_val = get_city_name
        # if db_get_city:
        #    city_id = db_get_city.city_id

    else:
        return {
            "Status": "FAILED",
            "Error": "Not given city_id or city_name parameter",
        }, 402

    if not db_get_city:
        return {
            "Status": "Failed",
            "Error": f"Not found any city with {error} = {error_val}",
        }, 404

    # delete city here
    try:
        db.session.query(city_class.StopTime).filter(
            city_class.StopTime.city_id == db_get_city.city_id
        ).delete()

        db.session.commit()

        db.session.query(city_class.Trip).filter(
            city_class.Trip.city_id == db_get_city.city_id
        ).delete()

        db.session.commit()

        db.session.query(city_class.ControlStop).filter(
            city_class.ControlStop.city_id == db_get_city.city_id
        ).delete()
        db.session.query(city_class.Route).filter(
            city_class.Route.city_id == db_get_city.city_id
        ).delete()

        db.session.commit()

        db.session.query(city_class.Agency).filter(
            city_class.Agency.city_id == db_get_city.city_id
        ).delete()
        db.session.query(city_class.Calendar).filter(
            city_class.Calendar.city_id == db_get_city.city_id
        ).delete()
        db.session.query(city_class.RouteType2).filter(
            city_class.RouteType2.city_id == db_get_city.city_id
        ).delete()
        db.session.query(city_class.Stop).filter(
            city_class.Stop.city_id == db_get_city.city_id
        ).delete()
        db.session.query(city_class.Variant).filter(
            city_class.Variant.city_id == db_get_city.city_id
        ).delete()
        db.session.query(city_class.VehicleType).filter(
            city_class.VehicleType.city_id == db_get_city.city_id
        ).delete()
        db.session.query(city_class.Shape).filter(
            city_class.Shape.city_id == db_get_city.city_id
        ).delete()

        db.session.commit()

        db.session.query(City).filter(City.city_id == db_get_city.city_id).delete()

        db.session.commit()
    except exc.IntegrityError as integrity_error:
        db.session.rollback()
        return {
            "Status": "Failed",
            "Error": f"Cannot delete city {db_get_city.city_name} (id = {db_get_city.city_id})",
            "integrity_error": integrity_error,
        }, 409
    else:
        return (
            {
                "Status": "Success",
                "Content": f"Succesfully deleted city \
{db_get_city.city_name} (city_id = {db_get_city.city_id})",
            },
            202,
        )


@app.route("/routes", methods=["GET"])
def get_routes():
    """
    API ENDPOINT
    Reciving:
    city_id (*)
    (*) - Required

    Returning:
    {"city": name, "routes": [{<route> #TODO}, {...}]}
    """

    if "city_id" not in request.args:
        return {"Status": "FAILED", "Error": "Not given city_id parameter"}, 402
    get_city_id = request.args.get("city_id")

    db_get_city = City.query.filter_by(city_id=get_city_id).first()
    db_get_routes = Route.query.filter_by(city_id=get_city_id).all()

    if not db_get_city:
        return {
            "Status": "Failed",
            "Error": f"Not found any city with id {get_city_id}",
        }, 404
    if not db_get_routes:
        return {
            "Status": "Failed",
            "Error": f"Not found any route for city with id {get_city_id}",
        }, 404

    return {
        "city": db_get_city.city_name,
        "routes": [route.get_dict() for route in db_get_routes],
    }


@app.route("/stop/nearest", methods=["GET"])
def get_stop_nearest():
    """
    API ENDPOINT
    Reciving:
    - city_id *
    - age *
    - coordinates ** or
    - location **
    *-required
    **-required one of

    Returns:
    my_location - info about recieved data
    distance_to_stops -
        list of 5 closests stop
        in range of max distance for age
        with data:
            - distance (from my_location to stop in km)
            - stop_id
            - stop_name
    """
    # GETTING PARAMS
    if "city_id" not in request.args:
        return {
            "Status": "Failed",
            "Error": "Missing required parameter: 'city_id'",
        }, 400

    if "age" not in request.args:
        return {"Status": "Failed", "Error": "Missing required parameter: 'age'"}, 400

    get_city_id = request.args.get("city_id")
    get_age = request.args.get("age")

    if "location" in request.args:
        try:
            get_coordinates = location_to_cords(request.args.get("location"))
        except AttributeError as error:
            return {"Status": "Failed", "Error": str(error)}, 404
    elif "coordinates" not in request.args:
        return {
            "Status": "Failed",
            "Error": "Missing required parameter: 'location' or 'coordinates'",
        }, 400
    else:
        get_coordinates = tuple(
            request.args.get("coordinates").replace(" ", "").split(",")
        )

    # ENDPOINT OPERATIONS
    my_location = GeoPoint(get_coordinates, get_city_id, get_age)

    return {
        "my_location": my_location.__dict__,
        "top_5_closests_stops": [
            {
                "stop_name": stop["stop"].stop_name,
                "stop_id": stop["stop"].stop_id,
                "distance": stop["distance"],
            }
            for stop in my_location.distance_to_stops()[:5]
        ],
    }


@app.route("/stop/nearest/departures", methods=["GET"])
def get_stop_nearest_departures():
    """
    API ENDPOINT
    Reciving:
    - city_id *
    - age *
    - coordinates ** or
    - location **
    - time ** #if not given is current time
    *-required
    **-required one of

    Returns:
    my_location - info about recieved data
    distance_to_stops -
        list of 5 closests stop
        in range of max distance for age
        with data:
            - distance (from my_location to stop in km)
            - stop_id
            - stop_name
            - next_departure_time
            - next_departure_line
            - next_departure_direction
    """
    # GETTING PARAMS
    if "city_id" not in request.args:
        return {
            "Status": "Failed",
            "Error": "Missing required parameter: 'city_id'",
        }, 400

    if "age" not in request.args:
        return {"Status": "Failed", "Error": "Missing required parameter: 'age'"}, 400

    get_city_id = request.args.get("city_id")
    get_age = request.args.get("age")

    if "location" in request.args:
        try:
            get_coordinates = location_to_cords(request.args.get("location"))
        except AttributeError as error:
            return {"Status": "Failed", "Error": str(error)}, 404
    elif "coordinates" not in request.args:
        return {
            "Status": "Failed",
            "Error": "Missing required parameter: 'location' or 'coordinates'",
        }, 400
    else:
        get_coordinates = tuple(
            request.args.get("coordinates").replace(" ", "").split(",")
        )

    if "departure_time" in request.args:
        get_departure_time = datetime.strptime(
            request.args.get("departure_time"), "%Y-%m-%d %H:%M"
        )
    else:
        get_departure_time = datetime.now()

    # ENDPOINT OPERATIONS
    my_location = GeoPoint(get_coordinates, get_city_id, get_age)

    return {
        "my_location": my_location.__dict__,
        "top_5_closests_stops": [
            {
                "stop_name": stop["stop"].stop_name,
                "stop_id": stop["stop"].stop_id,
                "distance": stop["distance"],
                "next_departures": [
                    {
                        "line": next_departure.trip.route_id,
                        "time": next_departure.departure_time.strftime("%H:%M:%S"),
                        "direction": next_departure.trip.route.get_direction(
                            next_departure.trip.direction_id
                        ),
                    }
                    for next_departure in stop["next_departure"]
                ],
            }
            for stop in my_location.stop_next_departure(get_departure_time)
        ],
    }


@app.route("/trip/connection", methods=["GET"])
def get_trip_connection():
    """
    API ENDPOINT
    Reciving:
        - city_id *
        - age *
        - start_coordinates ** or
        - start_location **
        AND
        - end_coordinates ** or
        - end_location **
        - departure_time ** #if not given is current time
    *-required
    **-required one of

    Returns:
        start: details about start point
        end: details about end point
        connections [list of next possible connections
        with data:
            - direction
            - line
            - FROM {
                departure_time,
                stop name
            }
            - TO {
                arrival_time,
                stop_name
            }
        ]
    """
    # GETTING PARAMS
    if "city_id" not in request.args:
        return {
            "Status": "Failed",
            "Error": "Missing required parameter: 'city_id'",
        }, 400

    if "age" not in request.args:
        return {"Status": "Failed", "Error": "Missing required parameter: 'age'"}, 400

    get_city_id = request.args.get("city_id")
    get_age = request.args.get("age")

    if "start_location" in request.args:
        try:
            get_start_coordinates = location_to_cords(
                request.args.get("start_location")
            )
        except AttributeError as error:
            return {"Status": "Failed", "Error": str(error)}, 404
    elif "start_coordinates" not in request.args:
        return {
            "Status": "Failed",
            "Error": "Missing required parameter: 'start_location' or 'start_coordinates'",
        }, 400
    else:
        get_start_coordinates = tuple(
            request.args.get("start_coordinates").replace(" ", "").split(",")
        )

    if "end_location" in request.args:
        try:
            get_end_coordinates = location_to_cords(request.args.get("end_location"))
        except AttributeError as error:
            return {"Status": "Failed", "Error": str(error)}, 404
    elif "end_coordinates" not in request.args:
        return {
            "Status": "Failed",
            "Error": "Missing required parameter: 'end_location' or 'end_coordinates'",
        }, 400
    else:
        get_end_coordinates = tuple(
            request.args.get("end_coordinates").replace(" ", "").split(",")
        )

    if "departure_time" in request.args:
        get_departure_time = datetime.strptime(
            request.args.get("departure_time"), "%Y-%m-%d %H:%M"
        )
    else:
        get_departure_time = datetime.now()

    # ENDPOINT OPERATIONS
    start_location = GeoPoint(get_start_coordinates, get_city_id, get_age)
    end_location = GeoPoint(get_end_coordinates, get_city_id, get_age)

    route_find = FindRoute(start_location, end_location)

    try:
        connections = route_find.find_connection(get_departure_time)
    except RuntimeError as error:
        return {"Status": "Failed", "Error": str(error)}, 404

    return {
        "starting point": route_find.start.__dict__,
        "ending point": route_find.end.__dict__,
        "connections": [
            {
                "FROM": stop_time.details(),
                "TO": route_find.find_end_stop(stop_time).details(
                    time_to_return="arrival"
                ),
                "line": stop_time.trip.route_id,
                "direction": stop_time.trip.route.get_direction(
                    stop_time.trip.direction_id
                ),
            }
            for stop_time in connections
            if route_find.find_end_stop(stop_time)
        ],
    }

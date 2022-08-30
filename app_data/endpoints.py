"""Endpoint for api"""
#import jsonify

from app_data import app
from app_data.feed_data import Feed
from app_data.app_constants import FEED_FILE_NAME, FEED_LOCATION, TEMP_CITIES_LIST


@app.route("/", methods=["GET"])
@app.route("/get_api_version", methods=["GET"])
def get_api_version():
    """Returns api and feeds version"""
    cities = {city: Feed(FEED_LOCATION+city+'/'+FEED_FILE_NAME).__dict__  for city in TEMP_CITIES_LIST}

    return {"api_version": "0.0.1", "cities": cities}


@app.route("/routes/test", methods=["GET"])
def routes_test():
    """JUST TESTING ENDPOINT"""
    try:
        feed_info = Feed("./wroclaw/feed_info.txt")
    except FileNotFoundError:
        return {"error_message": "Cannot find file"}
    else:
        return {"feed_info": feed_info.is_feed_outdated()}

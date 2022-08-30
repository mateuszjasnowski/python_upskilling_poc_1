"""Endpoint for api"""
# import jsonify

from app_data import app
from app_data.feed_data import Feed, download_feed


FEED_FILE = "./wroclaw/feed_info.txt"


def __init__():
    try:
        feed = Feed(FEED_FILE)
    except FileNotFoundError:
        print("No file found ...")

        feed = download_feed()
    else:
        if feed.is_feed_outdated():
            print("Current feed is outdated ...")
            feed = download_feed()
    finally:
        if not feed.is_feed_outdated():
            print("Feed up to date ...")
        print("inizializing app")


__init__()


@app.route("/", methods=["GET"])
@app.route("/get_api_version", methods=["GET"])
def get_api_version():
    """Returns api and feed version"""
    feed = Feed(FEED_FILE)
    return {"api_version": "0.0.1", "feed_content": feed.__dict__}


@app.route("/routes/test", methods=["GET"])
def routes_test():
    """JUST TESTING ENDPOINT"""
    try:
        feed_info = Feed("./wroclaw/feed_info.txt")
    except FileNotFoundError:
        return {"error_message": "Cannot find file"}
    else:
        return {"feed_info": feed_info.is_feed_outdated()}

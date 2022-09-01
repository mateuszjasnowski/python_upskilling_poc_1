"""PoC API App for MPK data"""
from app_data.feed_data import feed_checker
from app_data import app
from app_data.app_constants import (
    FEED_FILE_NAME,
    FEED_LOCATION,
    TEMP_CITIES_LIST,
    FEED_URL,
)


def main():
    """
    Executing feed version check
    THEN
    Starting app
    """
    if feed_checker(TEMP_CITIES_LIST, FEED_LOCATION, FEED_FILE_NAME, FEED_URL):
        print("=== APP STARTING ===")
        app.run(host="127.0.0.1", debug=True)
    else:
        print("FATAL: Cannot start app due failed one or more feed update")


if __name__ == "__main__":
    main()

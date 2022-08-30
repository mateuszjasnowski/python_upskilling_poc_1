"""PoC API App for MPK data"""
from app_data.app_constants import (
    FEED_FILE_NAME,
    FEED_LOCATION,
    TEMP_CITIES_LIST,
    FEED_URL,
)
from app_data.feed_data import Feed, download_feed
from app_data import app


def feed_checker(): #TODO unittest
    """
    Checking if cities' feeds are up to date
    IF NOT: trying to update them
    """
    downloaded_feeds = []
    for city in TEMP_CITIES_LIST:
        feed = None
        try:
            feed = Feed(FEED_LOCATION + city + "/" + FEED_FILE_NAME)
        except FileNotFoundError:
            print(f"FATAL: {city} feed not found ...")
            feed = download_feed(FEED_URL, FEED_LOCATION + city)
        else:
            if feed != None and feed.is_feed_outdated():
                print(f"ERROR: {city} feed is outdated ...")
                feed = download_feed(FEED_URL, FEED_LOCATION + city)
        finally:
            if feed != None and not feed.is_feed_outdated():
                print(f"OK: {city} feed up to date ...")
                downloaded_feeds.append(True)
            else:
                downloaded_feeds.append(False)

    if False in set(downloaded_feeds): #Fail if even one feed update fails
        print(downloaded_feeds)
        return False
    return True


def main():
    """
    Executing feed version check
    THEN
    Starting app
    """
    if feed_checker():
        print("=== APP STARTING ===")
        app.run(host="127.0.0.1", debug=True)
    else:
        print("FATAL: Cannot start app due failed one or more feed update")


if __name__ == "__main__":
    main()

'''PoC API App for MPK data'''
from app_data.app_constants import FEED_FILE_NAME, FEED_LOCATION, TEMP_CITIES_LIST, FEED_URL
from app_data.feed_data import Feed, download_feed
from app_data import app

def feed_checker():
    for city in TEMP_CITIES_LIST:
        try:
            feed = Feed(FEED_LOCATION+city+'/'+FEED_FILE_NAME)
        except FileNotFoundError:
            print("FATAL: {} feed not found ...".format(city))

            feed = download_feed(FEED_URL, FEED_LOCATION+city)
        else:
            if feed.is_feed_outdated():
                print("EROOR: {} feed is outdated ...".format(city))
                feed = download_feed(FEED_URL, FEED_LOCATION+city)
        finally:
            if not feed.is_feed_outdated():
                print("OK: {} feed up to date ...".format(city))

def main():
    feed_checker()
    print("=== APP STARTING ===")
    app.run(host='127.0.0.1', debug=True)


if __name__ == "__main__":
    main()

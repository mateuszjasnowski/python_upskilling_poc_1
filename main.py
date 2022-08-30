"""PoC API App for MPK data"""
from app_data.feed_data import feed_checker
from app_data import app


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

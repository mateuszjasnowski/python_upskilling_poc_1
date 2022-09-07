"""PoC API App for MPK data"""
from app_data import app
from app_data.secrets import API_URL, API_PORT


def main():
    """
    TODO
    """
    app.run(host=API_URL, port=API_PORT, ssl_context='adhoc', debug=True)


if __name__ == "__main__":
    main()

"""PoC API App for MPK data"""
from app_data import app
from app_data.secrets import API_URL, API_PORT

def main():
    """
    starting app with proper setings
    """
    app.run(host=API_URL, port=API_PORT, ssl_context='adhoc')

if __name__ == "__main__":
    main()
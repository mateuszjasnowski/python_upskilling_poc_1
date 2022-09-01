import urllib.request
import zipfile
import os

from flask import request

from app_data import app
from app_data.city import CityData

@app.route("/cities/create_city", methods=["POST"])
def cities_create_city():
    request_data = request.args
    city_name = str(request_data["city_name"])
    #city_url = str(request_data["city_url"])

    '''
    #get city data here
    try:
        print(f"ACTION: Downloading files for {city_name} from {city_url} ...")
        zip_file_name = ".temp_city.zip"
        temp_city_dict = '.temp_city/'

        #download the file
        urllib.request.urlretrieve(city_url, zip_file_name)

        #unzip the file
        with zipfile.ZipFile(zip_file_name, "r") as zip_ref:
            zip_ref.extractall(temp_city_dict)

        # remove zip file TODO or remove zip and directory later
        os.remove(zip_file_name)
    except Exception:
        print("FAILED: Cannot download feed")
        raise TimeoutError("FAILED: Cannot download feed")
    else:
        #do next steps if downloading not fails
        return "test"
    '''
    city_data = CityData(city_name=city_name)

    return {'Status': "Success", city_name: city_data.__dict__}, 201
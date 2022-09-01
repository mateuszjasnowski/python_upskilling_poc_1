'''
Module contains City class and all needed methods to operate with them
'''
import os
import shutil
import zipfile
import urllib.request

class CityData():
    """CityData downloaded from web"""
    def __init__(self, city_name: str, city_url: str, download_mode: bool = True) -> None:
        '''
        Download city's data from web and upload to DB
        For city's data representation, use City class
        Actions in __init__:
        - try to download files
        - unpack zip archive
        - get needed data from files inside
        - upload data to db
        '''
        self.errors = []
        self.return_code = 201

        temp_city_dict = '.temp_city/'
        try:
            if download_mode == True:
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
            self.errors.append("Cannot download feed")
            self.return_code = 500
        else:
            #opening files
            try:
                with open(temp_city_dict+'routes.txt', 'r', encoding="UTF-8") as routes_file:
                    file_lines = routes_file.read().replace('"', "").split("\n")
                    file_columns = file_lines[0].split(",")
                self.routes = [dict(zip(file_columns, line.split(','))) for line in file_lines[1:]]

            except FileNotFoundError as not_found:
                self.errors.append(f'Cannot open file {not_found.filename}')
                self.return_code = 500
            finally:
                self.name = city_name
                if download_mode == True:
                    os.remove(zip_file_name)
                    shutil.rmtree(temp_city_dict)

    def items(self) -> str:
        return {'name': self.name, 'num or routes': len(self.routes)}

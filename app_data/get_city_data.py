"""
Downloading city data
Unpacking files
Geting needed data
Uploading to DB
"""
import os
import shutil
import zipfile
import urllib.request
from os import listdir
from os.path import isfile, join


class CityData:
    """CityData downloaded from web"""

    def __init__(
        self, city_name: str, city_url: str, download_mode: bool = True
    ) -> None:
        """
        Download city's data from web and upload to DB
        For city's data representation, use City class
        Actions in __init__:
        - try to download files
        - unpack zip archive
        - get needed data from files inside
        - upload data to db
        """
        self.errors = []
        self.return_code = 201

        temp_city_dict = ".temp_city/"

        #downloading
        try:
            if download_mode is True:
                print(f"ACTION: Downloading files for {city_name} from {city_url} ...")
                zip_file_name = ".temp_city.zip"
                temp_city_dict = ".temp_city/"

                # download the file
                urllib.request.urlretrieve(city_url, zip_file_name)

                # unzip the file
                with zipfile.ZipFile(zip_file_name, "r") as zip_ref:
                    zip_ref.extractall(temp_city_dict)

        except Exception:
            self.errors.append("Cannot download feed")
            self.return_code = 500

        else:
            # opening files
            self.file_list = [f for f in listdir(temp_city_dict) if isfile(join(temp_city_dict, f))]

            for file in self.file_list:
                get_data_errors, file_content = self.get_data_from_file(file_name=temp_city_dict+file)
                if get_data_errors != '':
                    self.errors.append(get_data_errors)
                    self.return_code = 500
                setattr(self, file.replace('.txt',''), file_content)

            self.name = city_name

        finally:
                if download_mode is True:
                    os.remove(zip_file_name)
                    shutil.rmtree(temp_city_dict)

    def get_data_from_file(self, file_name: str) -> str | list:
        errors = ''
        try:
                with open(
                    file_name, "r", encoding="utf-8-sig" #BOM encoding with UTF-8
                ) as routes_file:
                    file_lines = routes_file.read().replace('"', "").split("\n")
                    file_columns = file_lines[0].split(",")
                file_content = [
                    dict(zip(file_columns, line.split(","))) for line in file_lines[1:]
                    if line != ""
                ]

        except FileNotFoundError as not_found:
            errors = f"Cannot open file {not_found.filename}"
            file_content = 'Not avalible'
        finally:
            return errors, file_content


    def items(self) -> dict:
        """Returing dict with visible items"""
        return {"name": self.name, "rows in files": {file: len(getattr(self, file.replace('.txt', ''))) for file in self.file_list}}

# pylint: disable=E1101
"""
Downloading city data
Unpacking files
Geting needed data
Uploading to DB
"""
import os
import shutil
from urllib.error import URLError
import zipfile
import urllib.request
from os import listdir
from os.path import isfile, join
from datetime import datetime

import app_data.city
from app_data import db


class FileData:
    """FileData object contins file's content and errors recieved from opening file"""

    def __init__(self, file_name):
        self.errors = ""
        try:
            with open(
                file_name, "r", encoding="utf-8-sig"  # BOM encoding with UTF-8
            ) as routes_file:
                file_lines = routes_file.read().replace('"', "").split("\n")
                file_columns = file_lines[0].split(",")
            self.file_content = [
                dict(zip(file_columns, line.split(",")))
                for line in file_lines[1:]
                if line != ""
            ]

        except FileNotFoundError as not_found:
            self.errors = f"Cannot open file {not_found.filename}"
            self.file_content = "Not avalible"
            # raise FileNotFoundError(f"Cannot open file {not_found.filename}")


class CityData:
    """CityData downloaded from web"""

    def __init__(
        self,
        city_name: str,
        city_url: str,
        download_mode: bool = True,
        city_dir: str = ".temp_city/",
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

        # downloading
        try:
            if download_mode is True:
                print(f"ACTION: Downloading files for {city_name} from {city_url} ...")
                zip_file_name = ".temp_city.zip"
                city_dir = ".temp_city/"

                # download the file
                urllib.request.urlretrieve(city_url, zip_file_name)

                # unzip the file
                with zipfile.ZipFile(zip_file_name, "r") as zip_ref:
                    zip_ref.extractall(city_dir)

        except URLError:
            self.errors.append("Cannot download feed")
            self.return_code = 500

        else:
            # opening files
            self.file_list = [f for f in listdir(city_dir) if isfile(join(city_dir, f))]

            if len(self.file_list) == 0:
                self.errors.append("No files found!")
                self.return_code = 204
            else:
                for file in self.file_list:
                    file_data = FileData(city_dir + file)
                    get_data_errors = file_data.errors
                    file_content = file_data.file_content
                    if get_data_errors != "":
                        self.errors.append(get_data_errors)
                        self.return_code = 500
                    setattr(self, file.replace(".txt", ""), file_content)

            self.name = city_name

        finally:
            try:
                if download_mode is True:
                    os.remove(zip_file_name)
                    shutil.rmtree(city_dir)
            except FileNotFoundError as error:
                self.errors.append(f"Cannot delete file/s {error.filename}")

    def insert_to_db(self, city_id):
        """Inserting cities' attributes to db"""
        agencies = [
            app_data.city.Agency(
                city_id=city_id,
                agency_id=agency["agency_id"],
                agency_name=agency["agency_name"],
                agency_url=agency["agency_url"],
                agency_timezone=agency["agency_timezone"],
                agency_phone=agency["agency_phone"],
                agency_lang=agency["agency_lang"],
            )
            for agency in self.agency
        ]

        stops = [
            app_data.city.Stop(
                city_id=city_id,
                stop_id=stop["stop_id"],
                stop_code=stop["stop_code"],
                stop_name=stop["stop_name"],
                stop_lat=stop["stop_lat"],
                stop_lon=stop["stop_lon"],
            )
            for stop in self.stops
        ]

        calendars = [
            app_data.city.Calendar(
                city_id=city_id,
                service_id=calendar["service_id"],
                monday=calendar["monday"],
                tuesday=calendar["tuesday"],
                wednesday=calendar["wednesday"],
                thursday=calendar["thursday"],
                friday=calendar["friday"],
                saturday=calendar["saturday"],
                sunday=calendar["sunday"],
                start_date=datetime.strptime(calendar["start_date"], "%Y%m%d"),
                end_date=datetime.strptime(calendar["end_date"], "%Y%m%d"),
            )
            for calendar in self.calendar
        ]

        control_stops = [
            app_data.city.ControlStop(
                city_id=city_id,
                variant_id=control_stop["variant_id"],
                stop_id=control_stop["stop_id"],
            )
            for control_stop in self.control_stops
        ]

        route_types = [
            app_data.city.RouteType2(
                city_id=city_id,
                route_type2_id=route_type["route_type2_id"],
                route_type2_name=route_type["route_type2_name"],
            )
            for route_type in self.route_types
        ]

        routes = [
            app_data.city.Route(
                city_id=city_id,
                route_id=route["route_id"],
                agency_id=route["agency_id"],
                route_short_name=route["route_short_name"],
                route_long_name=route["route_long_name"],
                route_desc=route["route_desc"],
                route_type=route["route_type"],
                route_type2_id=route["route_type2_id"],
                valid_from=datetime.strptime(route["valid_from"], "%Y-%m-%d"),
                valid_until=datetime.strptime(route["valid_until"], "%Y-%m-%d"),
            )
            for route in self.routes
        ]

        time_convert = (
            lambda t: f"{str(int(t.split(':')[0])%24)}:{t.split(':')[1]}:{t.split(':')[2]}"
        )
        stop_times = [
            app_data.city.StopTime(
                city_id=city_id,
                trip_id=str(stop_time["trip_id"]),
                arrival_time=datetime.strptime(
                    time_convert(stop_time["arrival_time"]), "%H:%M:%S"
                ).time(),
                departure_time=datetime.strptime(
                    time_convert(stop_time["departure_time"]), "%H:%M:%S"
                ).time(),
                stop_id=stop_time["stop_id"],
                stop_sequence=stop_time["stop_sequence"],
                pickup_type=stop_time["pickup_type"],
                drop_off_type=stop_time["drop_off_type"],
            )
            for stop_time in self.stop_times
        ]

        variants = [
            app_data.city.Variant(
                city_id=city_id,
                variant_id=variant["variant_id"],
                is_main=variant["is_main"],
            )
            for variant in self.variants
        ]

        vehicle_types = [
            app_data.city.VehicleType(
                city_id=city_id,
                vehicle_type_id=vehicle_type["vehicle_type_id"],
                vehicle_type_name=vehicle_type["vehicle_type_name"],
                vehicle_type_description=vehicle_type["vehicle_type_description"],
                vehicle_type_symbol=vehicle_type["vehicle_type_symbol"],
            )
            for vehicle_type in self.vehicle_types
        ]

        trips = [
            app_data.city.Trip(
                city_id=city_id,
                route_id=trip["route_id"],
                service_id=trip["service_id"],
                trip_id=trip["trip_id"],
                trip_headsign=trip["trip_headsign"],
                direction_id=trip["direction_id"],
                shape_id=trip["shape_id"],
                brigade_id=trip["brigade_id"],
                variant_id=trip["variant_id"],
            )
            for trip in self.trips
        ]

        for agency in agencies:
            db.session.add(agency)

        for calendar in calendars:
            db.session.add(calendar)

        for route_type in route_types:
            db.session.add(route_type)

        for stop in stops:
            db.session.add(stop)

        for variant in variants:
            db.session.add(variant)

        for vehicle_type in vehicle_types:
            db.session.add(vehicle_type)

        db.session.commit()  # commit to 1st-layer tables
        inserted_rows = len(agencies) +\
            len(calendars) +\
            len(route_types) +\
            len(stops) +\
            len(variants) +\
            len(vehicle_types)

        print(f"ACTION: inserting {inserted_rows} rows to 6 tables")

        for control_stop in control_stops:
            db.session.add(control_stop)

        for route in routes:
            db.session.add(route)

        db.session.commit()  # commit to 2nd-layer tables
        inserted_rows = len(control_stops) + len(routes)
        print(f"ACTION: inserting {inserted_rows} rows to 2 tables")

        for trip in trips:
            db.session.add(trip)

        db.session.commit()  # commit to 3nd-layer tables
        print(f"ACTION: inserting {len(trips)} rows to 1 table")

        for stop_time in stop_times:
            db.session.add(stop_time)

        # try:
        db.session.commit()  # commit to 4th-layer tables
        print(f"ACTION: inserting {len(stop_times)} rows to 1 table")
        # except exc.IntegrityError as ie:
        #        db.session.rollback()
        #        if ie.orig  and len(str(ie.orig).split('\n')) > 1:
        #            print(str(ie.orig).split('\n')[1])
        #        else:
        #            print(f'ERROR: cannot insert row with id {new_row.service_id}, skipping!')
        return True

    def items(self) -> dict:
        """Returing dict with visible items"""
        return {
            "name": self.name,
            "rows in files": {
                file: len(getattr(self, file.replace(".txt", "")))
                for file in self.file_list
            },
        }

"""
Unittests for find_route module
Testing FindRoute class with all methods
"""
import unittest

from sqlalchemy import exc

from app_data.find_route import FindRoute
from app_data.geo_point import GeoPoint
from app_data.get_city_data import CityData
from app_data import db
import app_data.city as city


class TestFindRoute(unittest.TestCase):
    """
    Testing FindRoute object inizialization
    !!!DB Connection needed!!!
    """

    @classmethod
    def setUpClass(cls) -> None:
        """setup objects for class"""

        try:
            db.inspect(db.engine)
        except exc.OperationalError:
            cls.db_connected = False
        else:
            cls.db_connected = True

        cls.download_mode = False
        cls.city_dir = "./unittests/cities_test_set/"
        cls.city_name = "test_city_2"
        cls.city_url = "http://172.0.0.1"

        test_set_3 = cls.city_dir + "test_city_3_db/"

        if cls.db_connected:
            print("TEST DEBUG: DB is responding.")
            cls.test_set_3 = CityData(
                cls.city_name, cls.city_url, cls.download_mode, city_dir=test_set_3
            )

            if not city.City.query.filter_by(city_id=5).first():
                print("TEST DEBUG: Not found city with id 5 in db")
                new_city = city.City(city_id=5, city_name=cls.city_name)
                try:
                    print("TEST DEBUG: Adding city with city_id = 5 do DB")
                    db.session.add(new_city)
                    db.session.commit()
                except exc.IntegrityError as integrity_error:
                    db.session.rollback()
                    print(f"TEST ERROR: Failed \n{integrity_error}")
                    cls.test_city_in_db = False
                else:
                    print("TEST DEBUG: Success")
                    cls.city_id = (
                        city.City.query.filter_by(city_name=cls.city_name)
                        .first()
                        .city_id
                    )
                try:
                    print("TEST DEBUG: Inserting data to city_id 5")
                    cls.test_city_in_db = cls.test_set_3.insert_to_db(cls.city_id)
                except exc.IntegrityError as integrity_error:
                    db.session.rollback()
                    db.session.query(city.City).filter(
                        city.City.city_id == cls.city_id
                    ).delete()
                    db.session.commit()
                    print(f"TEST ERROR: Failed \n{integrity_error}")
                    cls.test_city_in_db = False

                    if not cls.test_city_in_db:
                        print("TEST DEBUG: Deleting city with city_id = 5")
                        db.session.query(city.City).filter(
                            city.City.city_id == cls.city_id
                        ).delete()
                        db.session.commit()
            else:
                print("TEST DEBUG: City with city_id = 5 found in DB")
                cls.city_id = 5
                cls.test_city_in_db = True

        if cls.db_connected:
            # points age 23
            cls.point_1 = GeoPoint((51.119804400436536, 16.99132523967443), 5, 23)
            cls.point_2 = GeoPoint((51.11161724679465, 17.02185645157625), 5, 23)

            # points age 35
            cls.point_3 = GeoPoint((51.11710159154701, 17.038304679302943), 5, 35)
            cls.point_4 = GeoPoint((51.141548149234325, 17.034398121740978), 5, 35)

            # age 75
            cls.point_5 = GeoPoint((51.11428853446852, 17.04703580165012), 5, 75)
            cls.point_6 = GeoPoint((51.10935876837617, 17.0351224031273), 5, 75)

    def setUp(self) -> None:
        """Action executed on every test instance"""

        # making sure that DB connection was established
        self.assertTrue(self.db_connected, "DB not connected")
        # making sure that test_city_3 is in DB
        self.assertTrue(self.test_city_in_db, "Set test_set_3 not in DB")

    def test_test_case(self):
        pass  # TODO

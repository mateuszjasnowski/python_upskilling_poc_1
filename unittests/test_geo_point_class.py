"""
Unittests for geo_point class
Testing class with methods
"""
# TODO create test_city_2 with static data
import unittest

from sqlalchemy import exc

from app_data import db
from app_data.geo_point import GeoPoint
from app_data.get_city_data import CityData
import app_data.city as city


class TestGeoPoint(unittest.TestCase):
    """Testing GeoPoint object inizialization"""

    @classmethod
    def setUpClass(cls) -> None:
        """setup objects for class"""
        cls.geo_point_1 = GeoPoint((51.10881271500856, 17.03415783285653), 1, 15)
        cls.geo_point_2 = GeoPoint((51.11735339830748, 16.997283957364438), 1, 70)
        cls.geo_point_3 = GeoPoint((51.09872492804073, 17.036577040546952), 1, 23)
        cls.geo_point_4 = GeoPoint((51.09872492804073, 17.036577040546952), 1, 300)

    def test_object_init(self):
        """Checking created GeoPoint type"""

        self.assertTrue(isinstance(self.geo_point_1, GeoPoint))
        self.assertTrue(isinstance(self.geo_point_2, GeoPoint))
        self.assertTrue(isinstance(self.geo_point_3, GeoPoint))
        self.assertTrue(isinstance(self.geo_point_4, GeoPoint))

    def test_max_distance_calculation(self):
        """Testing max_distance calculation"""

        self.assertEqual(self.geo_point_1.max_distance, 1)
        self.assertEqual(self.geo_point_2.max_distance, 0.1)
        self.assertEqual(self.geo_point_3.max_distance, 5)
        self.assertEqual(self.geo_point_4.max_distance, 0.1)

    def test_not_enough_args(self):
        """Testing error raise if not enough args were given"""

        try:
            test_point = GeoPoint((51.0987, 17.03652), 1)
        except Exception as error:
            self.assertTrue(isinstance(error, TypeError))
        else:
            self.assertTrue(not isinstance(test_point, GeoPoint))

    def test_wrong_cords_given(self):
        """Testing error raise if cords were given in wrong format"""
        try:
            test_point = GeoPoint([0, 0], 1, 20)
        except TypeError as error:
            self.assertTrue(isinstance(error, TypeError))
        else:
            self.assertTrue(not isinstance(test_point, GeoPoint))


class TestDistanceToStop(unittest.TestCase):
    """
    !!!DB CONNECTION REQUIRED!!!
    Testing distance_to_stops method
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
            cls.geo_point_1 = GeoPoint((51.10881271500856, 17.03415783285653), 1, 15)
            cls.geo_point_2 = GeoPoint((51.11735339830748, 16.997283957364438), 1, 70)
            cls.geo_point_3 = GeoPoint((51.09872492804073, 17.036577040546952), 1, 23)
            cls.geo_point_4 = GeoPoint((51.09872492804073, 17.036577040546952), 1, 300)

    def setUp(self) -> None:
        """Action executed on every test instance"""

        # making sure that DB connection was established
        self.assertTrue(self.db_connected, "DB not connected")
        # making sure that test_city_3 is in DB
        self.assertTrue(self.test_city_in_db, "Set test_set_3 not in DB")

    def test_for_next_do(self):
        """TODO"""
        print(len(self.geo_point_1.distance_to_stops()))


class TestStopNextDeparture(unittest.TestCase):
    """TODO POSSIBLE OFFLINE WORKING"""

    def test_test_case(self):
        """TODO"""
        pass


if __name__ == "__main__":
    unittest.main()

"""
Unittests for geo_point class
Testing class with methods
"""
# TODO create test_city_2 with static data
import unittest

from sqlalchemy import exc

from app_data import db
from app_data.geo_point import GeoPoint


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

        if cls.db_connected:
            cls.geo_point_1 = GeoPoint((51.10881271500856, 17.03415783285653), 1, 15)
            cls.geo_point_2 = GeoPoint((51.11735339830748, 16.997283957364438), 1, 70)
            cls.geo_point_3 = GeoPoint((51.09872492804073, 17.036577040546952), 1, 23)
            cls.geo_point_4 = GeoPoint((51.09872492804073, 17.036577040546952), 1, 300)

    def setUp(self) -> None:
        """Action executed on every test instance"""

        self.assertTrue(self.db_connected, "DB not connected")

    def test_test_case(self):
        """TODO"""
        print(len(self.geo_point_1.distance_to_stops()))


class TestStopNextDeparture(unittest.TestCase):
    """TODO POSSIBLE OFFLINE WORKING"""

    def test_test_case(self):
        """TODO"""
        pass


if __name__ == "__main__":
    unittest.main()

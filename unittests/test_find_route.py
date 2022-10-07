"""
Unittests for find_route module
Testing FindRoute class with all methods
"""
import unittest
from datetime import datetime

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
            point_1 = GeoPoint((51.119804400436536, 16.99132523967443), 5, 23)
            point_2 = GeoPoint((51.11161724679465, 17.02185645157625), 5, 23)
            print("TEST DEBUG: test_route_1.__init__")
            cls.test_route_1 = FindRoute(point_1, point_2)

            # points age 35
            point_3 = GeoPoint((51.11710159154701, 17.038304679302943), 5, 35)
            point_4 = GeoPoint((51.141548149234325, 17.034398121740978), 5, 35)
            print("TEST DEBUG: test_route_2.__init__")
            cls.test_route_2 = FindRoute(point_3, point_4)

            # age 75
            point_5 = GeoPoint((51.11428853446852, 17.04703580165012), 5, 75)
            point_6 = GeoPoint((51.10935876837617, 17.0351224031273), 5, 75)
            print("TEST DEBUG: test_route_3.__init__")
            cls.test_route_3 = FindRoute(point_5, point_6)

    def setUp(self) -> None:
        """Action executed on every test instance"""

        # making sure that DB connection was established
        self.assertTrue(self.db_connected, "DB not connected")
        # making sure that test_city_3 is in DB
        self.assertTrue(self.test_city_in_db, "Set test_set_3 not in DB")

    def test_object_init(self):
        """Testing __init__ method of object"""

        # object type check
        print("TEST DEBUG: type check")
        self.assertIsInstance(self.test_route_1, FindRoute)
        self.assertIsInstance(self.test_route_2, FindRoute)
        self.assertIsInstance(self.test_route_3, FindRoute)

        # object attributes check
        print("TEST DEBUG: attributes check")
        self.assertIsInstance(self.test_route_1.start, GeoPoint)
        self.assertIsInstance(self.test_route_1.end, GeoPoint)
        self.assertIsInstance(self.test_route_1.stops_in_start_range, list)
        self.assertIsInstance(self.test_route_1.stops_in_end_range, list)

        self.assertIsInstance(self.test_route_2.start, GeoPoint)
        self.assertIsInstance(self.test_route_2.end, GeoPoint)
        self.assertIsInstance(self.test_route_1.stops_in_start_range, list)
        self.assertIsInstance(self.test_route_1.stops_in_end_range, list)

        self.assertIsInstance(self.test_route_3.start, GeoPoint)
        self.assertIsInstance(self.test_route_3.end, GeoPoint)
        self.assertIsInstance(self.test_route_1.stops_in_start_range, list)
        self.assertIsInstance(self.test_route_1.stops_in_end_range, list)

        # attributes lenght check
        print("TEST DEBUG: attributes lenght check")
        self.assertGreater(len(self.test_route_1.stops_in_start_range), 0)
        self.assertGreater(len(self.test_route_1.stops_in_end_range), 0)

        self.assertGreater(len(self.test_route_2.stops_in_start_range), 0)
        self.assertGreater(len(self.test_route_2.stops_in_end_range), 0)

        self.assertEqual(len(self.test_route_3.stops_in_start_range), 0)
        self.assertEqual(len(self.test_route_3.stops_in_end_range), 0)

    def test_direct_trip_lines_true_scenario(self):
        """Testing _is_direction_correct local method"""
        # type check
        print("TEST DEBUG: type check")
        self.assertIsInstance(self.test_route_1._direct_trip_lines(), set)
        self.assertIsInstance(self.test_route_2._direct_trip_lines(), set)

        self.assertIsInstance(list(self.test_route_1._direct_trip_lines())[0], str)
        self.assertIsInstance(list(self.test_route_2._direct_trip_lines())[0], str)

        # lenght check
        print("TEST DEBUG: lenght check")
        self.assertGreater(len(self.test_route_1._direct_trip_lines()), 0)
        self.assertGreater(len(self.test_route_2._direct_trip_lines()), 0)

    def test_direct_trip_lines_empty_scenario(self):
        """Testing _is_direction_correct in not found connection scenario"""

        self.assertRaises(RuntimeError, self.test_route_3._direct_trip_lines)

    def test_is_direction_correct(self):
        """Testing _is_direction_correct method"""

        # test vars
        # ROUTE 1
        print("TEST DEBUG: Creating test vars for route_1")
        stop_time_id_1 = 630362
        stop_time_1 = city.StopTime.query.filter_by(
            city_id=self.city_id, stop_time_id=stop_time_id_1
        ).first()

        #!Not test but proper test var confirmation
        self.assertIsNot(
            stop_time_1,
            None,
            f"TEST ERROR: Cannot find StopTime \
with conditions: city_id = {self.city_id} \
& stop_time_id = {stop_time_id_1}",
        )

        # ROUTE 2
        print("TEST DEBUG: Creating test vars for route_2")
        stop_time_id_2 = 671778
        stop_time_2 = city.StopTime.query.filter_by(
            city_id=self.city_id, stop_time_id=stop_time_id_2
        ).first()

        #!Not test but proper test var confirmation
        self.assertIsNot(
            stop_time_2,
            None,
            f"TEST ERROR: Cannot find StopTime \
with conditions: city_id = {self.city_id} \
& stop_time_id = {stop_time_id_2}",
        )

        # TEST
        print("TEST DEBUG: Testing returned values")
        self.assertTrue(self.test_route_1._is_direction_correct(stop_time_1))
        self.assertTrue(self.test_route_2._is_direction_correct(stop_time_2))

    def test_find_connection_correct_scenario(self):
        """
        Testing find_connection method
        Using scenarios for possible connections to found
        """

        test_date = datetime(2022, 9, 30, 20, 15, 0)

        connection_1 = self.test_route_1.find_connection(test_date)
        connection_2 = self.test_route_2.find_connection(test_date)

        self.assertIsInstance(connection_1, list)
        self.assertIsInstance(connection_2, list)

        self.assertGreater(len(connection_1), 0)
        self.assertGreater(len(connection_2), 0)

        self.assertIsInstance(connection_1[0], city.StopTime)
        self.assertIsInstance(connection_2[0], city.StopTime)

        if len(connection_1) > 1:
            self.assertLessEqual(
                connection_1[0].departure_time, connection_1[1].departure_time
            )

        if len(connection_2) > 1:
            self.assertLessEqual(
                connection_2[0].departure_time, connection_2[1].departure_time
            )

    def test_find_connection_not_correct_scenario(self):
        """
        Testing find_connection method
        Using scenario where conenction cannot be found
        """

        test_date = datetime(2022, 9, 30, 20, 15, 0)

        try:
            connection = self.test_route_3.find_connection(test_date)
        except Exception as error:
            self.assertIsInstance(error, RuntimeError)
        else:
            self.assertIsInstance(connection, None)

    def test_find_end_stop_correct_scenario(self):
        """
        Testing find_end_stop method
        Passing correct stop_time args
        """

        # test vars
        # ROUTE 1
        print("TEST DEBUG: Creating test vars for route_1")
        stop_time_id_1 = 630362
        stop_time_1 = city.StopTime.query.filter_by(
            city_id=self.city_id, stop_time_id=stop_time_id_1
        ).first()

        #!Not test but proper test var confirmation
        self.assertIsNot(
            stop_time_1,
            None,
            f"TEST ERROR: Cannot find StopTime \
with conditions: city_id = {self.city_id} \
& stop_time_id = {stop_time_id_1}",
        )

        # ROUTE 2
        print("TEST DEBUG: Creating test vars for route_2")
        stop_time_id_2 = 671778
        stop_time_2 = city.StopTime.query.filter_by(
            city_id=self.city_id, stop_time_id=stop_time_id_2
        ).first()

        self.assertIsNot(
            stop_time_2,
            None,
            f"TEST ERROR: Cannot find StopTime \
with conditions: city_id = {self.city_id} \
& stop_time_id = {stop_time_id_2}",
        )

        # TEST ACIONS
        end_stop_1 = self.test_route_1.find_end_stop(stop_time_1)

        self.assertIsInstance(end_stop_1, city.StopTime)
        self.assertEqual(end_stop_1.stop_time_id, 630366)
        self.assertEqual(stop_time_1.trip_id, end_stop_1.trip_id)

        end_stop_2 = self.test_route_2.find_end_stop(stop_time_2)
        self.assertEqual(end_stop_2, None)

    def test_find_end_stop_wrond_scenario(self):
        """
        Testing find_end_stop method
        Passing wrong stop_time args
        """

        # ROUTE 1
        print("TEST DEBUG: Creating test vars for route_1")
        stop_time_id_1 = 614560
        stop_time_1 = city.StopTime.query.filter_by(
            city_id=self.city_id, stop_time_id=stop_time_id_1
        ).first()

        #!Not test but proper test var confirmation
        self.assertIsNot(
            stop_time_1,
            None,
            f"TEST ERROR: Cannot find StopTime \
with conditions: city_id = {self.city_id} \
& stop_time_id = {stop_time_id_1}",
        )

        # TEST
        self.assertEqual(self.test_route_1.find_end_stop(stop_time_1), None)

        # ROUTE 2
        print("TEST DEBUG: Creating test vars for route_2")
        stop_time_id_2 = 668041
        stop_time_2 = city.StopTime.query.filter_by(
            city_id=self.city_id, stop_time_id=stop_time_id_2
        ).first()

        #!Not test but proper test var confirmation
        self.assertIsNot(
            stop_time_2,
            None,
            f"TEST ERROR: Cannot find StopTime \
with conditions: city_id = {self.city_id} \
& stop_time_id = {stop_time_id_2}",
        )

        # TEST
        self.assertEqual(self.test_route_2.find_end_stop(stop_time_2), None)

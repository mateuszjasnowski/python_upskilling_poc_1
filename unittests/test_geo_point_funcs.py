"""
Unittests for geo_point module's functions
Testing location_to_cords and distance_to_point funcs
"""

import unittest
import time
import warnings

from geopy.exc import GeocoderTimedOut

from app_data.geo_point import location_to_cords, distance_to_point, GeoPoint


class TestLocationToCords(unittest.TestCase):
    """Testing location_to_cords function"""

    def test_correct_address_wroclaw(self):
        """testing location_to_cords on correct locations from wrocław"""
        test_addresses = [
            {"address": "Wrocław", "cords": (51.1089776, 17.0326689)},
            {"address": "Legnicka 48H, Wrocław", "cords": (51.1170067, 16.9973544)},
            {
                "address": "Sukiennice 14/15, 50-029 Wrocław",
                "cords": (51.1096932, 17.0325215),
            },
            {
                "address": "Graniczna 190, 54-530 Wrocław",
                "cords": (51.1094747, 16.8810328),
            },
            {"address": "Długa, Wrocław", "cords": (51.118053, 17.0167744)},
        ]

        for location in test_addresses:
            self.assertEqual(location_to_cords(location["address"]), location["cords"])

    def test_incorrect_format_address(self):
        """Testing incorrect address format"""
        test_addresses = [
            {"address": "Wrocław", "cords": (51.1089776, 17.0326689)},
            {"address": "Wrocław, Długa", "cords": (51.118053, 17.0167744)},
            {
                "address": "Wrocław 51-618, Wystawowa 1",
                "cords": (51.1068875, 17.07731848674789),
            },
            {
                "address": "2A Namysłowska, Wrocław 50-304",
                "cords": (51.1256576, 17.0456567),
            },
        ]
        for location in test_addresses:
            self.assertEqual(location_to_cords(location["address"]), location["cords"])

    def test_location_as_name(self):
        """Testing location name instead of address"""
        test_addresses = [
            {
                "address": "Magnolia Park Wrocław",
                "cords": (51.1191288, 16.988824458129542),
            },
            {
                "address": "Hala Stulecia, Wrocław",
                "cords": (51.1068875, 17.07731848674789),
            },
            {
                "address": "Tarczyński Arena, Wrocław",
                "cords": (51.141186149999996, 16.943806687526074),
            },
            {
                "address": "Most Tumski, Wrocław",
                "cords": (51.1147184, 17.04226539467509),
            },
            {
                "address": "Wieża ciśnień, Wrocław",
                "cords": (51.08531365, 17.01759015267851),
            },
        ]

        for location in test_addresses:
            self.assertEqual(location_to_cords(location["address"]), location["cords"])

    def test_incorrect_locations(self):
        """Testing not existing locations"""
        test_addresses = [
            "Most tumski, Wrocław",
            "Nieisniejąca 15, 55-555 Wrocław",
            "Tytusa Bomby, 0125 Pacanów",
        ]

        for location in test_addresses:
            try:
                location_to_cords(location)
            except Exception as error:
                self.assertEqual(type(error), AttributeError)


class TestDistanceToPoint(unittest.TestCase):
    """Testing distance_to_point function"""

    def setUp(self) -> None:
        """Code executed at the begining of tc"""
        self.correct_points = [
            {
                "a": (0, 0),  # point a coordinats
                "b": (1, 1),  # point b coordinats
                "km": 156.89956829134027,  # expected value for km
                "mil": 97.4928718107131,  # expected value for miles
            },
            {"a": (0, 0), "b": (0, 0), "km": 0.0, "mil": 0.0},
            {
                "a": (-7.11543, -17.82725),
                "b": (-35.30073, -97.63799),
                "km": 8635.116689582885,
                "mil": 5365.612752514618,
            },
            {
                "a": (4.49999, -132.14469),
                "b": (29.05834, 150.14671),
                "km": 8577.641671092279,
                "mil": 5329.899431751246,
            },
            {
                "a": (51.109657, 17.030238),
                "b": (51.11049745627834, 17.0335354084796),
                "km": 0.24913360809119878,
                "mil": 0.1548044470860169,
            },
        ]

    def test_distance_between_points_km(self):
        """
        Testing distance betweent point a and b
        with kilomiter unit (default)
        """

        for point in self.correct_points:
            try:
                distance = distance_to_point(point["a"], point["b"])
            except GeocoderTimedOut:
                print("1st try failed, retrying afret 30s")
                time.sleep(30)
                try:
                    distance = distance_to_point(point["a"], point["b"])
                except GeocoderTimedOut:
                    print("Cannot check distance after 2nd try!")
            finally:
                self.assertEqual(distance, point["km"])
                time.sleep(1)

    def test_distance_between_points_miles(self):
        """
        Testing distance betweent point a and b
        with miles as unit argument
        """

        for point in self.correct_points:
            try:
                distance = distance_to_point(point["a"], point["b"], unit="miles")
            except GeocoderTimedOut:
                print("1st try failed, retrying afret 30s")
                time.sleep(30)
                try:
                    distance = distance_to_point(point["a"], point["b"], unit="miles")
                except GeocoderTimedOut:
                    print("Cannot check distance after 2nd try!")
            finally:
                self.assertEqual(distance, point["mil"])
                time.sleep(1)

    def test_not_correct_values(self):
        """
        Testing not correct values
        and raised exceptions
        """

        not_correct_points = [
            {
                "a": (91, 10),  # point a coordinats
                "b": (90, 0),  # point b coordinats
            },
            {"a": 0, "b": 0},
            {"a": (-91, 90), "b": (0, 0)},
        ]

        for point in not_correct_points:
            warnings.simplefilter("ignore")
            try:
                distance = distance_to_point(point["a"], point["b"])
            except Exception as error:
                self.assertTrue(isinstance(error, ValueError))
            else:
                self.assertTrue(isinstance(distance, None))


if __name__ == "__main__":
    unittest.main()

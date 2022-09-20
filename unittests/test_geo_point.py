"""
Unittests for geo_poiint module
Testing GeoPoint class with all methods
Testing location_to_cords and distance_to_point funcs
"""
from cgi import test
import unittest

from app_data.geo_point import location_to_cords, distance_to_point, GeoPoint

class TestLocationToCords(unittest.TestCase):
    """Testing location_to_cords function"""

    def test_correct_address_wroclaw(self):
        """testing location_to_cords on correct locations from wrocław"""
        test_addresses = [
            {
                "address": "Wrocław",
                "cords": (51.1089776, 17.0326689)
            },
            {
                "address": "Legnicka 48H, Wrocław",
                "cords": (51.1170067, 16.9973544)
            },
            {
                "address": "Sukiennice 14/15, 50-029 Wrocław",
                "cords": (51.1096932, 17.0325215)
            },
            {
                "address": "Graniczna 190, 54-530 Wrocław",
                "cords": (51.1094747, 16.8810328)
            },
            {
                "address": "Długa, Wrocław",
                "cords": (51.118053, 17.0167744)
            }
        ]

        for location in test_addresses:
            self.assertEqual(location_to_cords(location['address']), location['cords'])

    def test_incorrect_format_address(self):
        test_addresses = [
            {
                "address": "Wrocław",
                "cords": (51.1089776, 17.0326689)
            },
        ]
        #for location in test_addresses:
            #self.assertEqual(location_to_cords(location['address']), location['cords'])

import unittest
import os

from app_data.feed_data import feed_checker


class TestFeedData(unittest.TestCase):
    def test_feed_checker(self):
        FEED_LOCATION = "./unittests/cities/"
        FEED_FILE_NAME = "feed_info.txt"
        TEMP_CITIES_LIST = ["city_a"]
        FEED_URL = ''
        self.assertEqual(feed_checker(TEMP_CITIES_LIST, FEED_LOCATION, FEED_FILE_NAME, FEED_URL), True)

        TEMP_CITIES_LIST = ["city_b"]
        self.assertEqual(feed_checker(TEMP_CITIES_LIST, FEED_LOCATION, FEED_FILE_NAME, FEED_URL), False)
        self.assertEqual(feed_checker(TEMP_CITIES_LIST, FEED_LOCATION, FEED_FILE_NAME, FEED_URL), True)


if __name__ == '__main__':
    unittest.main()

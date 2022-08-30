import unittest
import os

from app_data.feed_data import feed_checker

class TestFeedData(unittest.TestCase):
    def setUp(self): #TODO why not working
        os.rename('./app_data/app_constants.py','./app_data/app_constants.back.py')
        with open('./unittests/app_constants.py', 'r') as app_consts:
            with open('./app_data/app_constants.py', 'w') as new_content:
                new_content.writelines(app_consts.readlines())

    def test_feed_checker(self):
        self.assertEqual(feed_checker(), True)

    def tearDown(self):
        os.remove('./app_data/app_constants.py')
        os.rename('./app_data/app_constants.back.py','./app_data/app_constants.py')

if __name__ == '__main__':
    unittest.main()

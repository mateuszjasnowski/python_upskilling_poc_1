"""
Unittests for get_city_data module
Testing FileData class and CityData class with all containing methods
"""
import unittest

from app_data.get_city_data import FileData, CityData


class TestFileData(unittest.TestCase):
    """Testing FileData class"""

    def setUp(self) -> None:
        """setup vars before every tests"""
        self.city_dir = "./unittests/cities_test_set/"  # dir of test sets

    def test_file_data_set_1_feed_info(self):
        """Testing feed_info.txt from test set #1"""
        city_dir = self.city_dir + "test_city_1/"
        file_data_object = FileData(city_dir + "feed_info.txt")

        self.assertEqual(type(file_data_object), FileData)
        self.assertEqual(file_data_object.errors, "")
        self.assertEqual(len(file_data_object.file_content), 1)

        # detailed checks
        self.assertEqual(type(file_data_object.file_content), list)
        self.assertEqual(
            file_data_object.file_content[0]["feed_publisher_name"], "UM Wrocław"
        )

    def test_file_data_set_1_routes(self):
        """Testing routes.txt from test set #1"""
        city_dir = self.city_dir + "test_city_1/"
        file_data_object = FileData(city_dir + "routes.txt")

        self.assertEqual(file_data_object.errors, "")
        self.assertEqual(len(file_data_object.file_content), 125)
        self.assertEqual(type(file_data_object.file_content), list)
        self.assertEqual(type(file_data_object.file_content[0]), dict)
        self.assertEqual(len(file_data_object.file_content[0]), 9)

    def test_file_data_set_not_exist(self):
        """Testing behaviour on empty test set"""
        city_dir = self.city_dir + "test_city_0/"
        file_data_object = FileData(city_dir + "feed_info.txt")

        self.assertEqual(
            file_data_object.errors,
            "Cannot open file ./unittests/cities_test_set/test_city_0/feed_info.txt",
        )
        self.assertEqual(file_data_object.file_content, "Not avalible")


class TestCityData(unittest.TestCase):
    """Testing CityData class"""

    @classmethod
    def setUpClass(cls) -> None:
        """Setup for class"""
        cls.download_mode = False
        cls.city_dir = "./unittests/cities_test_set/"
        cls.city_name = "test_city"
        cls.city_url = "http://172.0.0.1"

        test_set_0 = cls.city_dir + "test_city_0/"
        test_set_1 = cls.city_dir + "test_city_1/"

        cls.test_set_0 = CityData(
            cls.city_name, cls.city_url, cls.download_mode, city_dir=test_set_0
        )
        cls.test_set_1 = CityData(
            cls.city_name, cls.city_url, cls.download_mode, city_dir=test_set_1
        )

    def test_city_data_set_1(self):
        """Testing CityData.__init__() for data set 1"""
        city_data_object = self.test_set_1

        # all object parameters check
        self.assertEqual(city_data_object.errors, [])
        self.assertEqual(len(city_data_object.errors), 0)

        self.assertEqual(city_data_object.return_code, 201)
        self.assertEqual(len(city_data_object.file_list), 13)
        self.assertEqual(city_data_object.name, self.city_name)

    def test_city_data_set_0(self):
        """Testing CityData.__init__() for data set 0 (EMPTY)"""
        city_data_object = self.test_set_0

        self.assertTrue("No files found!" in city_data_object.errors)
        self.assertGreaterEqual(len(city_data_object.errors), 1)
        self.assertEqual(city_data_object.return_code, 204)
        self.assertEqual(city_data_object.name, self.city_name)
        self.assertEqual(len(city_data_object.file_list), 0)

    def test_city_data_items_set_1(self):
        """Testing .items() for data set 1"""
        city_data_object = self.test_set_1.items()

        self.assertEqual(type(city_data_object), dict)
        self.assertTrue("name" in city_data_object)
        self.assertTrue("rows in files" in city_data_object)
        self.assertEqual(city_data_object["name"], self.city_name)
        self.assertEqual(type(city_data_object["rows in files"]), dict)
        self.assertEqual(len(city_data_object["rows in files"]), 13)

    def test_city_data_items_set_0(self):
        """Testing .items() for data set 0 (empty)"""
        city_data_object = self.test_set_0.items()

        self.assertEqual(type(city_data_object), dict)
        self.assertTrue("name" in city_data_object)
        self.assertTrue("rows in files" in city_data_object)
        self.assertEqual(city_data_object["name"], self.city_name)
        self.assertEqual(type(city_data_object["rows in files"]), dict)
        self.assertEqual(len(city_data_object["rows in files"]), 0)


if __name__ == "__main__":
    unittest.main()

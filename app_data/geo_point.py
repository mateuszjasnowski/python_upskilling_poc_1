# pylint: disable=R0903, C3001
"""
Geo points class and operations on them
"""
from geopy import Nominatim
from geopy.location import Location
from geopy.distance import geodesic

from app_data.city import Stop


def location_to_cords(address: str) -> tuple:
    """Converting location's address to coordinates"""

    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(address)

    if isinstance(location, Location):
        return (location.latitude, location.longitude)

    raise AttributeError(f"location in type {type(location)} instead of Location")

class GeoPoint():
    """Geo location as reference point"""

    def __init__(self, coordinats: tuple, city_id: id, age: int) -> None:
        """Creating GeoPoint with coordinates of point and city_id to search in DB"""
        #self.latitute, self.longitutie = coordinats
        self.coordinates = coordinats
        self.city_id = city_id
        self.age = int(age)

        age_table = {
            range(0, 15+1): 1,
            range(16, 25+1): 5,
            range(26, 35+1): 2,
            range(36, 50+1): 1,
            range(51, 64+1): 0.5,
            range(65, 250+1): 0.1 #bigger than 64 ;)
        }

        self.max_distance = 0.1

        for age_range, max_distance in age_table.items():
            if self.age in age_range:
                self.max_distance = max_distance

    def top_5_closest_stops(self) -> list:
        """Returns list of 5 stops closest to geo point"""
        db_stops = Stop.query.filter_by(city_id = self.city_id).all()

        distance_to_point = lambda point: geodesic(self.coordinates, point).kilometers

        '''nearest_stops = sorted([
            stop for stop in db_stops
            if distance_to_point((stop.stop_lat, stop.stop_lon)) <= self.max_distance
            ], key=lambda d: d['distance'])

        distance_to_stop = [
            {
            "stop_name": stop.stop_name,
            "stop_id": stop.stop_id,
            "distance": distance_to_point((stop.stop_lat, stop.stop_lon)),
            }
            for stop in nearest_stops
            ]'''
        distance_to_stop = sorted([
            {
            "stop_name": stop.stop_name,
            "stop_id": stop.stop_id,
            "distance": distance_to_point((stop.stop_lat, stop.stop_lon))
            }
            for stop in db_stops
            if distance_to_point((stop.stop_lat, stop.stop_lon)) <= self.max_distance
        ],
        key=lambda d: d['distance']
        )

        return distance_to_stop[:5]

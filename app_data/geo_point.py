# pylint: disable=R0903, C3001
"""
Geo points class and operations on them
"""
from datetime import datetime

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

    raise AttributeError(f"Cannot find location {address}")


def distance_to_point(
    point_a: tuple, point_b: tuple, unit: str = "kilometers"
) -> float:
    """
    Reciving points a and b (tuples with cords)
    returns distance bettwen points
    """
    distance = geodesic(point_a, point_b)
    return getattr(distance, unit)


class GeoPoint:
    """Geo location as reference point"""

    def __init__(self, coordinats: tuple, city_id: id, age: int) -> None:
        """Creating GeoPoint with coordinates of point and city_id to search in DB"""
        # self.latitute, self.longitutie = coordinats
        if isinstance(coordinats, tuple):
            self.coordinates = coordinats
        else:
            raise TypeError(f"{coordinats} is not tuple")
        self.city_id = city_id
        self.age = int(age)

        age_table = {
            range(0, 15 + 1): 1,
            range(16, 25 + 1): 5,
            range(26, 35 + 1): 2,
            range(36, 50 + 1): 1,
            range(51, 64 + 1): 0.5,
            range(65, 250 + 1): 0.1,  # bigger than 64 ;)
        }

        self.max_distance = 0.1

        for age_range, max_distance in age_table.items():
            if self.age in age_range:
                self.max_distance = max_distance

    def distance_to_stops(self) -> list:
        """Returns list of stops with distance to geo point"""
        db_stops = Stop.query.filter_by(city_id=self.city_id).all()

        nearest_stops = sorted(
            [
                {
                    "stop": stop,
                    "distance": distance_to_point(
                        self.coordinates, (stop.stop_lat, stop.stop_lon)
                    ),
                }
                for stop in db_stops
                if distance_to_point(self.coordinates, (stop.stop_lat, stop.stop_lon))
                <= self.max_distance
            ],
            key=lambda d: d["distance"],
        )

        return nearest_stops

    def stop_next_departure(self, refference_time: datetime) -> list:
        """Returns list of stops with distance and next departure to geo point"""
        closest_stops = self.distance_to_stops()[:5]

        for stop in closest_stops:
            next_departure_time = min(
                [
                    stop_time.departure_time
                    for stop_time in stop["stop"].stop_times
                    if stop_time.departure_time > refference_time.time()
                    and stop_time.trip.service.week()[
                        refference_time.strftime("%A").lower()
                    ]
                    == 1
                ]
            )

            stop["next_departure"] = [
                stop_time
                for stop_time in stop["stop"].stop_times
                if stop_time.departure_time == next_departure_time
                and stop_time.trip.service.week()[
                    refference_time.strftime("%A").lower()
                ]
                == 1
            ]

        return closest_stops

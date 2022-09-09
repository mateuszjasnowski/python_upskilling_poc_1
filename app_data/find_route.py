"""Class and methods to calculate route"""
from datetime import datetime
from app_data.geo_point import GeoPoint

class FindRoute():
    """Route from point A to point B"""
    def __init__(self, point_A: GeoPoint, point_B: GeoPoint, departure_time: datetime) -> None:
        self.start = point_A
        self.end = point_B
        self.departure = departure_time

        stops_in_end_range = self.end.distance_to_stops()
        lines_in_range = []
        for stop in stops_in_end_range:
            for line in stop['stop'].get_lines():
                lines_in_range.append(line)
        self.lines_in_range = set(lines_in_range)

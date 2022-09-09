"""Class and methods to calculate route"""
from datetime import datetime
from app_data.geo_point import GeoPoint

class FindRoute():
    """Route from point A to point B"""
    def __init__(self, point_A: GeoPoint, point_B: GeoPoint, departure_time: datetime) -> None:
        self.start = point_A
        self.end = point_B
        self.departure = departure_time

    def direct_trip_lines(self):
        """returns set of lines witch allow direct connection between stops"""
        stops_in_start_range = self.start.distance_to_stops()
        stops_in_end_range = self.end.distance_to_stops()
        lines_in_range = []
        lines_in_start_range = []

        for stop in stops_in_start_range:
                    for line in stop['stop'].get_lines():
                        lines_in_start_range.append(line)

        for stop in stops_in_end_range:
            for line in stop['stop'].get_lines():
                if line in lines_in_start_range:
                    lines_in_range.append(line)

        if len(lines_in_range) == 0:
            raise RuntimeError("Cannot find any lines to direct connection between points")
        return set(lines_in_range)

    #TODO
    '''
    compare:
        stop_time on stops (from nearest to farest)
        if stop_time for line what is in direct_trip_lines:
            show trip  (stop_time have trip attr)
    '''

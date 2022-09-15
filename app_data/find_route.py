# pylint: disable=R0903
"""Class and methods to calculate route"""
from datetime import datetime
from app_data.city import StopTime
from app_data.geo_point import GeoPoint, distance_to_point


class FindRoute:
    """Route from point A to point B"""

    def __init__(self, point_a: GeoPoint, point_b: GeoPoint) -> None:
        self.start = point_a
        self.end = point_b

    def _direct_trip_lines(self):
        """returns set of lines witch allow direct connection between stops"""
        stops_in_start_range = self.start.distance_to_stops()
        stops_in_end_range = self.end.distance_to_stops()
        lines_in_range = []
        lines_in_start_range = []

        for stop in stops_in_start_range:
            for line in stop["stop"].get_lines():
                lines_in_start_range.append(line)

        for stop in stops_in_end_range:
            for line in stop["stop"].get_lines():
                if line in lines_in_start_range:
                    lines_in_range.append(line)

        if len(lines_in_range) == 0:
            raise RuntimeError(
                "Cannot find any lines to direct connection between points"
            )
        return set(lines_in_range)

    def _is_direction_correct(self, stop_time: StopTime) -> bool:
        """
        Checing if direction from stop_time is correct
        It's mean if next stop in route is closer to destination
        returns True
        if not - > False
        """

        start_to_end_distance = distance_to_point(
            self.start.coordinates, self.end.coordinates
        )

        try:
            next_stop = stop_time.next_stop().stop
            next_stop_to_end_distance = distance_to_point(
                (next_stop.stop_lat, next_stop.stop_lon), self.end.coordinates
            )
        except StopIteration as error:
            print(error)
        else:
            if start_to_end_distance > next_stop_to_end_distance:
                return True

        return False

    def find_connection(self, departure_time: datetime) -> list[StopTime]:
        """
        NEED TO BE OPTIMIZED
        returns departures for possible connections
        """
        direct_lines = self._direct_trip_lines()

        start_nearest_stop = self.start.distance_to_stops()

        connections = []

        for stop in start_nearest_stop:
            if len(connections) > 5:
                return connections
            stop_times = sorted(
                [
                    stop_time
                    for stop_time in stop["stop"].stop_times
                    if stop_time.departure_time > departure_time.time()
                ],
                key=lambda s_t: s_t.departure_time,
            )

            for stop_time in stop_times:
                if (
                    stop_time.trip.route_id in direct_lines
                    and self._is_direction_correct(stop_time)
                    and stop_time.trip.service.week()[
                        departure_time.strftime("%A").lower()
                    ]
                    == 1
                ):
                    connections.append(stop_time)
                    break

        return sorted(connections, key=lambda s_t: s_t.departure_time)

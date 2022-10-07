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

        # collect important data
        self.stops_in_start_range = self.start.distance_to_stops()[:10]
        self.stops_in_end_range = self.end.distance_to_stops()[:10]

    def _direct_trip_lines(self) -> set[str]:
        """returns set of lines witch allow direct connection between stops"""

        lines_in_range = []
        lines_in_start_range = []

        for stop in self.stops_in_start_range:
            for line in stop["stop"].get_lines():
                lines_in_start_range.append(line)

        for stop in self.stops_in_end_range:
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
            (stop_time.stop.stop_lat, stop_time.stop.stop_lon), self.end.coordinates
        )

        try:
            next_stop = stop_time.next_stop().stop
            next_stop_to_end_distance = distance_to_point(
                (next_stop.stop_lat, next_stop.stop_lon), self.end.coordinates
            )
        except StopIteration:
            return False
        else:
            if start_to_end_distance > next_stop_to_end_distance:
                return True

        return False

    def find_connection(self, departure_time: datetime) -> list[StopTime]:
        """
        returns departures for possible connections
        """

        direct_lines = self._direct_trip_lines()

        start_nearest_stop = self.stops_in_start_range

        connections = []
        trips = []

        for stop in start_nearest_stop:
            if len(connections) > 5:
                break
            stop_times = sorted(
                [
                    stop_time
                    for stop_time in stop["stop"].stop_times
                    if (
                        stop_time.departure_time > departure_time.time()
                        and stop_time.trip.route_id in direct_lines
                    )
                ],
                key=lambda s_t: s_t.departure_time,
            )

            i = 0
            for stop_time in stop_times:
                if i > 5:
                    break
                if (
                    self._is_direction_correct(stop_time) is True
                    and stop_time.trip.service.week()[
                        departure_time.strftime("%A").lower()
                    ]
                    == 1
                    and stop_time.trip_id not in trips
                ):
                    connections.append(stop_time)
                    trips.append(stop_time.trip_id)
                    i += 1

        return sorted(connections, key=lambda s_t: s_t.departure_time)

    def find_end_stop(self, stop_time: StopTime) -> StopTime:
        """returning stop_time for route started at given stop_time"""

        stops_to_exit = [stop["stop"].stop_name for stop in self.stops_in_end_range]
        exit_stop = [
            next_stop_time
            for next_stop_time in stop_time.trip.stop_times
            if (
                next_stop_time.stop_sequence > stop_time.stop_sequence
                and next_stop_time.stop.stop_name in stops_to_exit
            )
        ]

        try:
            return exit_stop[0]
        except IndexError:
            return None

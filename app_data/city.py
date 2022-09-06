"""
Module contains db classes for tables:
City - indicating city
Agency
Calendar
Calendar_dates #MISS THAT
Control_stops
Route_types
Routes
Shapes #MISS
Stop_times
Stops
Trips
Variants
vehicle_types
"""
from app_data import db


class City(db.Model):
    """city table"""

    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(), unique=True, nullable=False)
    feed_publisher_name = db.Column(db.String())
    feed_publisher_url = db.Column(db.String())
    feed_lang = db.Column(db.String())
    feed_start_date = db.Column(db.DateTime)
    feed_end_date = db.Column(db.DateTime)

    agencies = db.relationship("Agency", backref="agencies", lazy=True)

    def __repr__(self):
        return f"City('{self.city_id}', \
            '{self.city_name}', '{self.feed_publisher_name}',\
            '{self.feed_publisher_url}', '{self.feed_lang}',\
            '{self.feed_start_date}', '{self.feed_end_date}')"


class Agency(db.Model):  # 1-layer
    """agency table"""

    city_id = db.Column(db.Integer, db.ForeignKey("city.city_id"), nullable=False)
    agency_id = db.Column(db.Integer, primary_key=True)
    agency_name = db.Column(db.String())
    agency_url = db.Column(db.String())
    agency_timezone = db.Column(db.String())
    agency_phone = db.Column(db.String())
    agency_lang = db.Column(db.String())


class Calendar(db.Model):  # 1-layer
    """calendar table"""

    city_id = db.Column(db.Integer, db.ForeignKey("city.city_id"), nullable=False)
    service_id = db.Column(db.Integer, primary_key=True)
    monday = db.Column(db.Integer)
    tuesday = db.Column(db.Integer)
    wednesday = db.Column(db.Integer)
    thursday = db.Column(db.Integer)
    friday = db.Column(db.Integer)
    saturday = db.Column(db.Integer)
    sunday = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)


class ControlStop(db.Model):  # 2-layer
    """control_stop table"""

    city_id = db.Column(db.Integer, db.ForeignKey("city.city_id"), nullable=False)
    control_stop_id = db.Column(db.Integer, primary_key=True)
    variant_id = db.Column(db.Integer, db.ForeignKey("variant.variant_id"))
    stop_id = db.Column(db.Integer, db.ForeignKey("stop.stop_id"))


class RouteType2(db.Model):  # 1-layer
    """route_type2 table"""

    city_id = db.Column(db.Integer, db.ForeignKey("city.city_id"), nullable=False)
    route_type2_id = db.Column(db.Integer, primary_key=True)
    route_type2_name = db.Column(db.String())

    def __repr__(self) -> str:
        return f"RouteType2('{self.city_id.city_name}', \
            '{self.route_type2_id}', '{self.route_type2_name}'"


class Route(db.Model):  # 2-layer
    """route table"""

    city_id = db.Column(db.Integer, db.ForeignKey("city.city_id"), nullable=False)
    route_id = db.Column(db.String(), primary_key=True)
    agency_id = db.Column(db.Integer, db.ForeignKey("agency.agency_id"), nullable=False)
    route_short_name = db.Column(db.String())
    route_long_name = db.Column(db.String())
    route_desc = db.Column(db.Text)
    route_type = db.Column(db.Integer)
    route_type2_id = db.Column(
        db.Integer, db.ForeignKey("route_type2.route_type2_id"), nullable=False
    )
    valid_from = db.Column(db.DateTime)
    valid_until = db.Column(db.DateTime)


class StopTime(db.Model):  # 4th layer
    """stop_time table"""

    stop_time_id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey("city.city_id"), nullable=False)
    trip_id = db.Column(db.String(), db.ForeignKey("trip.trip_id"), nullable=False)
    arrival_time = db.Column(db.Time)
    departure_time = db.Column(db.Time)
    stop_id = db.Column(db.Integer, db.ForeignKey("stop.stop_id"), nullable=False)
    stop_sequence = db.Column(db.Integer)
    pickup_type = db.Column(db.Integer)
    drop_off_type = db.Column(db.Integer)


class Stop(db.Model):  # 1-layer
    """stop table"""

    city_id = db.Column(db.Integer, db.ForeignKey("city.city_id"), nullable=False)
    stop_id = db.Column(db.Integer, primary_key=True)
    stop_code = db.Column(db.String())
    stop_name = db.Column(db.String())
    stop_lat = db.Column(db.String())
    stop_lon = db.Column(db.String())


class Trip(db.Model):  # 3rd layer
    """trip table"""

    city_id = db.Column(db.Integer, db.ForeignKey("city.city_id"), nullable=False)
    route_id = db.Column(db.String(), db.ForeignKey("route.route_id"), nullable=False)
    service_id = db.Column(
        db.Integer, db.ForeignKey("calendar.service_id"), nullable=False
    )
    trip_id = db.Column(db.String(), primary_key=True)
    trip_headsign = db.Column(db.String())
    direction_id = db.Column(db.Integer)
    shape_id = db.Column(db.Integer)  # not integrarting shapes
    brigade_id = db.Column(db.String())
    vehicle = db.Column(db.Integer, db.ForeignKey("vehicle_type.vehicle_type_id"))
    variant_id = db.Column(
        db.Integer, db.ForeignKey("variant.variant_id"), nullable=False
    )


class Variant(db.Model):  # 1-layer
    """variant table"""

    city_id = db.Column(db.Integer, db.ForeignKey("city.city_id"), nullable=False)
    variant_id = db.Column(db.Integer, primary_key=True)
    is_main = db.Column(db.Integer)
    equiv_main_variant_id = db.Column(db.Integer)
    join_stop_id = db.Column(db.Integer)
    disjoin_stop_id = db.Column(db.Integer)


class VehicleType(db.Model):  # 1-layer
    """vehicle_type table"""

    city_id = db.Column(db.Integer, db.ForeignKey("city.city_id"), nullable=False)
    vehicle_type_id = db.Column(db.Integer, primary_key=True)
    vehicle_type_name = db.Column(db.String())
    vehicle_type_description = db.Column(db.String())
    vehicle_type_symbol = db.Column(db.String())

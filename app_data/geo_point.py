"""
Geo points class and operations on them
"""

def location_to_cords(location: str) -> tuple:
    pass

class GeoPoint():
    def __init__(self, coordinats: tuple) -> None:
        self.latitute = coordinats[0]
        self.longitutie = coordinats[1]
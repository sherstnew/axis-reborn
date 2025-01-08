class ConstructionAreas:
    def __init__(
            self,
            no_living_square,
            apartments,
            block_of_flats
    ):
        self.no_living_square: float = no_living_square
        self.apartments: float = apartments
        self.block_of_flats: float = block_of_flats


class TransportNetwork:
    def __init__(
            self,
            transport_in_hour,
            rush_hour,
            max_load
    ):
        self.transport_in_hour: float = transport_in_hour
        self.rush_hour: float = rush_hour
        self.max_load: float = max_load


class Station:
    def __init__(
            self,
            passengerflow_morning,
            passengerflow_evening,
            capacity
    ):
        self.passengerflow_morning: float = passengerflow_morning
        self.passengerflow_evening: float = passengerflow_evening
        self.capacity: float = capacity


class RegionParams:
    def __init__(
            self,
            percent_of_working_people: float,
            public_transport_usage: float,
            traffic_to_center: float,
            personal_transport_passenger_rate: float,
            road_percent_living_load: float,
            road_percent_working_load: float
    ):
        self.params: list[float] = [
            percent_of_working_people,
            public_transport_usage,
            traffic_to_center,
            personal_transport_passenger_rate,
            road_percent_living_load,
            road_percent_working_load
        ]

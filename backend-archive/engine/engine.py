from engine.data_interfaces import ConstructionAreas, TransportNetwork, Station, RegionParams
from numpy import array
from scipy.special import softmax


class Engine:
    def recalc_all_traffic(
            self,
            construction_areas: list[ConstructionAreas],
            all_public_transport_stations: list[Station],
            all_roads_traffic: list[TransportNetwork],
            roads_location: list[float],
            region_params: RegionParams
    ) -> (list, list):

        new_people = self._calc_new_people(construction_areas)
        new_road_traffic_count, new_public_transport_traffic_count = \
            self._implement_region_params(new_people, *region_params.params)

        public_transport_statistics = \
            self._calc_public_traffic(new_public_transport_traffic_count, all_public_transport_stations)
        roads_traffic_statistics = self._calc_roads_traffic(new_road_traffic_count, all_roads_traffic, roads_location)

        return public_transport_statistics, roads_traffic_statistics

    @staticmethod
    def _calc_new_people(
            construction_areas: list[ConstructionAreas]
    ) -> (float, float):
        new_living_people = 0
        new_working_people = 0
        for construction_area in construction_areas:
            new_living_people += construction_area.apartments / 25
            new_living_people += construction_area.block_of_flats / 45
            new_working_people += construction_area.no_living_square / 35
        return new_living_people, new_working_people

    @staticmethod
    def _implement_region_params(
            new_people: (float, float),
            percent_of_working_people: float,
            public_transport_usage: float,
            traffic_to_center: float,
            personal_transport_passenger_rate: float,
            road_percent_living_load: float,
            road_percent_working_load: float
    ) -> (float, float):
        new_living_people, new_working_people = new_people
        new_living_working_people = new_living_people * percent_of_working_people

        new_living_working_people_on_public_transport = new_living_working_people * public_transport_usage * \
                                                        road_percent_living_load
        new_work_working_people_on_public_transport = new_working_people * public_transport_usage * \
                                                      road_percent_working_load

        max_road_traffic = max(1 - traffic_to_center, traffic_to_center)
        roads_usage = 1 - public_transport_usage
        new_living_working_people_on_roads = new_living_working_people * roads_usage * road_percent_living_load
        new_work_working_people_on_roads = new_working_people * roads_usage * road_percent_working_load

        new_people_on_roads = (new_living_working_people_on_roads + new_work_working_people_on_roads) / \
                              personal_transport_passenger_rate * max_road_traffic
        new_people_on_public_transport = new_living_working_people_on_public_transport + \
                                         new_work_working_people_on_public_transport

        return new_people_on_roads, new_people_on_public_transport / 1000

    def _calc_public_traffic(
            self,
            new_public_transport_traffic: float,
            all_public_transport_stations: list[Station]
    ) -> (list, list):
        morning_public_transport_statistics = []
        morning_public_traffic_percentage = self._get_morning_public_traffic_percentage(all_public_transport_stations)
        for i in range(len(morning_public_traffic_percentage)):
            station, morning_percentage = all_public_transport_stations[i], morning_public_traffic_percentage[i]
            new_morning_traffic = \
                self._calc_station_traffic(station.passengerflow_morning, new_public_transport_traffic *
                                           morning_percentage)
            morning_public_traffic_statistics = self._make_morning_statistics(station, new_morning_traffic)
            morning_public_transport_statistics.append(morning_public_traffic_statistics)

        evening_public_transport_statistics = []
        evening_public_traffic_percentage = self._get_evening_public_traffic_percentage(all_public_transport_stations)
        for i in range(len(evening_public_traffic_percentage)):
            station, evening_percentage = all_public_transport_stations[i], evening_public_traffic_percentage[i]
            new_evening_traffic = \
                self._calc_station_traffic(station.passengerflow_evening, new_public_transport_traffic *
                                           evening_percentage)
            evening_public_traffic_statistics = self._make_evening_statistics(station, new_evening_traffic)
            evening_public_transport_statistics.append(evening_public_traffic_statistics)

        return morning_public_transport_statistics, evening_public_transport_statistics

    @staticmethod
    def _get_morning_public_traffic_percentage(
            stations: list[Station]
    ) -> list[float]:
        public_traffic_percentage_passengerflow = []
        all_passengerflow = sum(map(lambda x: x.passengerflow_morning, stations))
        for station in stations:
            percentage = station.passengerflow_morning / all_passengerflow
            public_traffic_percentage_passengerflow.append(percentage)
        return public_traffic_percentage_passengerflow

    @staticmethod
    def _get_evening_public_traffic_percentage(
            stations: list[Station]
    ) -> list[float]:
        public_traffic_percentage_passengerflow = []
        all_passengerflow = sum(map(lambda x: x.passengerflow_evening, stations))
        for station in stations:
            percentage = station.passengerflow_morning / all_passengerflow
            public_traffic_percentage_passengerflow.append(percentage)
        return public_traffic_percentage_passengerflow

    @staticmethod
    def _calc_station_traffic(
            old_traffic: float,
            new_area_traffic: float
    ) -> float:
        new_traffic = old_traffic + new_area_traffic
        return new_traffic

    @staticmethod
    def _make_morning_statistics(
            station: Station,
            new_morning_traffic: float
    ) -> list[float, float, float]:
        traffic_increase = new_morning_traffic - station.passengerflow_morning
        traffic_percentage = station.passengerflow_morning / station.capacity
        new_traffic_percentage = (traffic_increase + station.passengerflow_morning) / station.capacity
        traffic_percentage_increase = new_traffic_percentage - traffic_percentage
        return [traffic_increase, new_traffic_percentage, traffic_percentage_increase]

    @staticmethod
    def _make_evening_statistics(
            station: Station,
            new_evening_traffic: float
    ) -> list[float, float, float]:

        traffic_increase = new_evening_traffic - station.passengerflow_evening
        traffic_percentage = station.passengerflow_evening / station.capacity
        new_traffic_percentage = (traffic_increase + station.passengerflow_evening) / station.capacity
        traffic_percentage_increase = new_traffic_percentage - traffic_percentage

        return [traffic_increase, new_traffic_percentage, traffic_percentage_increase]

    def _calc_roads_traffic(
            self,
            new_road_transport_traffic: float,
            all_roads: list[TransportNetwork],
            roads_location: list[float]
    ) -> list:
        roads_traffic_statistics = []
        roads_traffic_percentage = self._get_road_traffic_percentage(all_roads, roads_location)
        for i in range(len(roads_traffic_percentage)):
            road, percentage = all_roads[i], roads_traffic_percentage[i]
            new_road_traffic = self._calc_road_traffic(road.transport_in_hour, new_road_transport_traffic * percentage)
            roads_traffic_statistic = self._make_road_traffic_statistics(road, new_road_traffic)
            roads_traffic_statistics.append(roads_traffic_statistic)

        return roads_traffic_statistics

    def _get_road_traffic_percentage(
            self,
            roads: list[TransportNetwork],
            roads_location: list[float]
    ) -> list:
        roads_location_softmax = self._softmax_calibration(roads_location)

        roads_traffic_percentage_passengerflow = []
        all_passengerflow = sum(map(lambda x: x.transport_in_hour, roads))
        for road in roads:
            percentage = road.transport_in_hour / all_passengerflow
            roads_traffic_percentage_passengerflow.append(percentage)
        roads_traffic_percentage_passengerflow = list(map(lambda x: x * 0.6, roads_traffic_percentage_passengerflow))
        roads_location_softmax = list(map(lambda x: x * 0.4, roads_location_softmax))
        for i in range(len(roads_location_softmax)):
            roads_traffic_percentage_passengerflow[i] += roads_location_softmax[i]
        return roads_traffic_percentage_passengerflow

    @staticmethod
    def _softmax_calibration(
            roads_location: list[float]
    ) -> list[float]:
        roads_location = list(map(lambda x: 1/x, roads_location))
        roads_location = array(roads_location)
        roads_location_softmax = softmax(roads_location).tolist()
        return roads_location_softmax

    @staticmethod
    def _calc_road_traffic(
            old_traffic: float,
            new_area_traffic: float
    ) -> float:
        new_traffic = old_traffic + new_area_traffic
        return new_traffic

    @staticmethod
    def _make_road_traffic_statistics(
            road: TransportNetwork,
            new_road_traffic: float
    ) -> list[float, float, float]:
        traffic_increase = new_road_traffic - road.transport_in_hour
        traffic_rush_hour = round(road.transport_in_hour / road.max_load, 1) * 10
        new_traffic_rush_hour = round((traffic_increase + road.transport_in_hour) / road.max_load, 1) * 10
        traffic_rush_hour_increase = new_traffic_rush_hour - traffic_rush_hour

        return [traffic_increase, new_traffic_rush_hour, traffic_rush_hour_increase]

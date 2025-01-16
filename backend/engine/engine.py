import os
from dotenv import load_dotenv
import geopy.distance
import pandas as pd
import requests
from engine.data_interfaces import ConstructionAreas

load_dotenv()

df_stations = pd.read_csv("engine/stations_passengerflow.csv", delimiter=";")
df_mcd = pd.read_csv("engine/mcd.csv", delimiter=";")
df_bus_stops = pd.read_csv("engine/bus_stops.csv", delimiter=";")

# CONSTANTS

percent_working_people = 0.55
percent_metro_mcd = 0.502
percent_bus = 0.294
percent_public_transport = 0.68

first_quartal_length = 91

mcd_middle_passengerflow = 8064

# people
apartment_ppl = 33
flats_ppl = 18
office_ppl = 4.5

# CONSTANTS


def calc_all_people(construction_area: ConstructionAreas):
    new_living_people = 0
    new_working_people = 0

    new_living_people += construction_area.apartments / apartment_ppl
    new_living_people += construction_area.block_of_flats / flats_ppl
    new_working_people += construction_area.no_living_square / office_ppl
    return new_living_people + new_working_people


def get_station_passengerflow(station: str):
    if station in df_stations["NameOfStation"].values:
        return (
            int(
                df_stations.loc[df_stations["NameOfStation"] == station][
                    "IncomingPassengers"
                ].values[0]
            )
            + int(
                df_stations.loc[df_stations["NameOfStation"] == station][
                    "IncomingPassengers"
                ].values[0]
            )
        ) // first_quartal_length
    elif station in df_mcd["StationName"].values:
        return mcd_middle_passengerflow
    return -1


def geo_data_to_coords(geoData):
    coords = geoData.split("[")[1].split("]")[0]
    longtitude = float(coords.split(", ")[0])
    latitude = float(coords.split(", ")[1])
    return (latitude, longtitude)


def get_nearest_metro_stations(latitude, longtitude, amount):
    stations_response = requests.get(
        f"https://geocode-maps.yandex.ru/1.x/?apikey={os.getenv('YANDEX_API_KEY')}&geocode={str(longtitude)}, {str(latitude)}&format=json&kind=metro&results={str(amount)}"
    ).json()

    stations = []

    for station in stations_response["response"]["GeoObjectCollection"][
        "featureMember"
    ]:
        new_station = {}

        new_station["name"] = (
            station["GeoObject"]["name"].replace("метро ", "").replace("станция ", "")
        )
        new_station["latitude"] = station["GeoObject"]["Point"]["pos"].split(" ")[1]
        new_station["longtitude"] = station["GeoObject"]["Point"]["pos"].split(" ")[0]

        stations.append(new_station)

    return stations


def get_nearest_bus_stops(latitude, longtitude, amount):
    stops = df_bus_stops.to_dict("records")
    all_stops = []
    used_stops_names = []
    for stop in stops[1::]:
        if stop["stop_name"] not in used_stops_names:
            distance = geopy.distance.geodesic(
                (latitude, longtitude), geo_data_to_coords(stop["geoData"])
            ).m
            all_stops.append({"name": stop["stop_name"], "distance": distance, "latitude": geo_data_to_coords(stop["geoData"])[0], "longtitude": geo_data_to_coords(stop["geoData"])[1]})
            used_stops_names.append(stop["stop_name"])

    sorted_stops = sorted(all_stops, key=lambda stop: stop["distance"])

    return sorted_stops[:amount]


def calc_stations_stops_traffic(all_traffic, center, stations, stops):
    new_stations = []
    new_stops = []
    stations_km = []
    stops_km = []

    for station in stations:
        stations_km.append(
            geopy.distance.geodesic(center, (station["latitude"], station["longtitude"])).km
        )

    for stop in stops:
        stops_km.append(stop["distance"])

    all_traffic = all_traffic * percent_public_transport

    stations_traffic = percent_metro_mcd * all_traffic
    stops_traffic = percent_bus * all_traffic
    
    print(stations_traffic)

    for i in range(len(stations)):
        station = stations[i]
        new_station = {}
        new_station["name"] = station["name"]
        new_station["delta_traffic"] = round(
            (stations_km[len(stations_km) - 1 - i] / sum(stations_km)) * stations_traffic
        )

        passengerflow = get_station_passengerflow(station["name"])
        if passengerflow != -1:
            new_station["delta_percent"] = (
                round((passengerflow + new_station["delta_traffic"]) * 100 / passengerflow)
                - 100
            )
            new_station["previous_traffic"] = passengerflow
            new_station["new_traffic"] = passengerflow + new_station["delta_traffic"]
        else:
            new_station["delta_percent"] = 0
            new_station["previous_traffic"] = 0
            new_station["delta_traffic"] = 0
            
        new_station["latitude"] = station["latitude"]
        new_station["longtitude"] = station["longtitude"]

        new_stations.append(new_station)

    for i in range(len(stops)):
        stop = stops[i]
        new_stop = {}
        new_stop["name"] = stop["name"]
        new_stop["traffic"] = round((stops_km[len(stops_km) - 1 - i] / sum(stops_km)) * stops_traffic)
        new_stop["latitude"] = stop["latitude"]
        new_stop["longtitude"] = stop["longtitude"]

        new_stops.append(new_stop)

    return new_stations, new_stops
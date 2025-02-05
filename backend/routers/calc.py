import math
from fastapi.routing import APIRouter
from data.models import InputDataSquare, InputDataPeople, OutputData
from engine.engine import calc_all_people, calc_stations_stops_traffic, get_nearest_bus_stops, get_nearest_metro_stations

router = APIRouter(prefix="/calc")

moscow_square = 2511
# km
moscow_stops = 22581

def calculate_area(points) -> float:
    """
    Вычисление площади ЖК по формуле Гаусса
    """
    area = 0.0
    n = len(points)
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    area = abs(area) / 2.0
    return area

@router.post('/square')
async def calc_data(input_data: InputDataSquare) -> OutputData:
  stops_amount = calculate_area(input_data.points) * (111.134861111 ** 2) * moscow_stops / moscow_square
  people = calc_all_people(input_data.construction_area)
  nearest_stops = get_nearest_bus_stops(input_data.center[0], input_data.center[1], math.ceil(stops_amount))
  nearest_stations = get_nearest_metro_stations(input_data.center[0], input_data.center[1])
  stations, stops = calc_stations_stops_traffic(round(people), input_data.center, nearest_stations, nearest_stops)
  return {"stations": stations, "people": round(people), "stops": stops}

@router.post('/people')
async def calc_data(input_data: InputDataPeople) -> OutputData:
  stops_amount = calculate_area(input_data.points) * (111.134861111 ** 2) * moscow_stops / moscow_square
  nearest_stops = get_nearest_bus_stops(input_data.center[0], input_data.center[1], math.ceil(stops_amount))
  nearest_stations = get_nearest_metro_stations(input_data.center[0], input_data.center[1])
  stations, stops = calc_stations_stops_traffic(input_data.people, input_data.center, nearest_stations, nearest_stops)
  return {"stations": stations, "people": input_data.people, "stops": stops}
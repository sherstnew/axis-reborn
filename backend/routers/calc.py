from fastapi.routing import APIRouter
from data.models import InputDataSquare, InputDataPeople, OutputData
from engine.engine import calc_all_people, calc_stations_stops_traffic, get_nearest_bus_stops, get_nearest_metro_stations

router = APIRouter(prefix="/calc")

@router.post('/square')
async def calc_data(input_data: InputDataSquare, stations_amount: int, stops_amount: int) -> OutputData:
  people = calc_all_people(input_data.construction_area)
  nearest_stops = get_nearest_bus_stops(input_data.center[0], input_data.center[1], stops_amount)
  nearest_stations = get_nearest_metro_stations(input_data.center[0], input_data.center[1], stations_amount)
  stations, stops = calc_stations_stops_traffic(round(people), input_data.center, nearest_stations, nearest_stops)
  return {"stations": stations, "people": round(people), "stops": stops}

@router.post('/people')
async def calc_data(input_data: InputDataPeople, stations_amount: int, stops_amount: int) -> OutputData:
  nearest_stops = get_nearest_bus_stops(input_data.center[0], input_data.center[1], stops_amount)
  nearest_stations = get_nearest_metro_stations(input_data.center[0], input_data.center[1], stations_amount)
  stations, stops = calc_stations_stops_traffic(input_data.people, input_data.center, nearest_stations, nearest_stops)
  return {"stations": stations, "people": input_data.people, "stops": stops}
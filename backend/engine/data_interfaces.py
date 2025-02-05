from pydantic import BaseModel
from typing import List, Tuple

class ConstructionAreas(BaseModel):
        no_living_square: float
        apartments: float
        block_of_flats: float

class BusStop(BaseModel):
        name: str
        latitude: float
        longtitude: float
        
class MetroStation(BaseModel):
        name: str
        latitude: float
        longtitude: float

# (0.57 - percent of working people, 0.70 - public transport usage, 0.8 - traffic to center, 1.2 - personal transport_passenger_rate, 0.1 - road_percent_living_load, 0.35 - road_percent_working_load)
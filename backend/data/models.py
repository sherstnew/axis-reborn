from pydantic import BaseModel
from typing import List, Tuple
from engine.data_interfaces import ConstructionAreas

class OutputStation(BaseModel):
    name: str
    delta_traffic: int
    delta_percent: int
    previous_traffic: int
    new_traffic: int
    latitude: float
    longtitude: float

class OutputStop(BaseModel):
    name: str
    traffic: int
    latitude: float
    longtitude: float

class InputDataSquare(BaseModel):
    center: Tuple[float, float]
    construction_area: ConstructionAreas
    
class InputDataPeople(BaseModel):
    center: Tuple[float, float]
    people: int
    
class OutputData(BaseModel):
    stations: List[OutputStation]
    stops: List[OutputStop]
    people: int
from datetime import datetime
from pydantic import conint
from beanie import Document
from typing import Optional


class TransportNetworkWorkload(Document):
    transport_in_hour: float | int
    rush_hour: int = conint(ge=1, le=10)
    max_load: float | int
    
    class Settings:
        name = "TransportNetworkWorkload"
        
        
    class Config:
        json_schema_extra = {
            "example": {
                # "date": datetime.now(),
                "transport_in_hour": 40,
                "rush_hour": 4,
                "max_load": 50,
                "road_location":[8, 10]
            }
        }

class WorkloadOnStation(Document):
    name: str
    passengerflow_mornind: float | int
    passengerflow_evening: float | int
    capacity: float | int
    
    class Settings:
        name = "WorkloadOnStation"
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Rimskay",
                "passengerflow_mornind": 16000,
                "passengerflow_evening": 13000,
                "capacity": 18000
            }
        }
        
        
class SquareBuild(Document):
    date: Optional[datetime] = datetime.now()
    count_houses: float | int
    no_living_square: float | int
    apartments: float | int
    block_of_flats: float | int
    
    coordinates: list[float]
    neeres_stations: list[WorkloadOnStation]
    roads: list[TransportNetworkWorkload]
    road_location: list[float]
    
    class Settings:
        name = "SquareBuild"
        
    class Config:
        json_schema_extra = {
            "example": {
                "date": datetime.now(),
                "count_houses": 0,
                "no_living_square": 100,
                "apartments": 50,
                "block_of_flats": 50,
                "coordinates": [59.851393, 30.301184],
                "neeres_stations": ["Rimskay", "Ilich Square"],
                "roads": ["Enthusiasts Higway", "MKAD"]
            }
        }


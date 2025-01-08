from fastapi.routing import APIRouter
from engine.engine import get_nearest_bus_stops, get_nearest_metro_stations

router = APIRouter(prefix="/objects")


@router.get("/stations")
async def get_stations(latitude: float, longtitude: float, amount: int):
    return get_nearest_metro_stations(latitude=latitude, longtitude=longtitude, amount=amount)

@router.get("/stops")
async def get_stops(latitude: float, longtitude: float, amount: int):
    return get_nearest_bus_stops(latitude=latitude, longtitude=longtitude, amount=amount)

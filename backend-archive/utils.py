from engine.engine import Engine
from data.models import SquareBuild
from engine.data_interfaces import ConstructionAreas, Station, TransportNetwork, RegionParams


async def analytics(sqbuild: SquareBuild):
    engine = Engine()

    return engine.recalc_all_traffic(
        construction_areas=[ConstructionAreas(
            no_living_square=sqbuild.no_living_square, apartments=sqbuild.apartments, block_of_flats=sqbuild.block_of_flats)],

        all_public_transport_stations=list(map(lambda x: Station(
            passengerflow_evening=x.passengerflow_evening, passengerflow_morning=x.passengerflow_mornind, capacity=x.capacity), sqbuild.neeres_stations)),

        all_roads_traffic=list(map(lambda x: TransportNetwork(
            transport_in_hour=x.transport_in_hour, rush_hour=x.rush_hour, max_load=x.max_load), sqbuild.roads)),

        roads_location=sqbuild.road_location,
        
        region_params=RegionParams(0.57, 0.70, 0.8, 1.2, 0.1, 0.35))

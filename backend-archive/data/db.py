import motor.motor_asyncio
from data.config import REFERENCE
from beanie import init_beanie
from data.models import SquareBuild, TransportNetworkWorkload, WorkloadOnStation#, RegionParams


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        REFERENCE
    )

    await init_beanie(database=client.DriveHack, document_models=[SquareBuild])
    await init_beanie(database=client.DriveHack, document_models=[TransportNetworkWorkload])
    await init_beanie(database=client.DriveHack, document_models=[WorkloadOnStation])    

from data.db import SquareBuilds
import asyncio
from pprint import pprint

async def fgh():
    a =await SquareBuilds.find().to_list(length=10)
    
    return a

pprint(type(asyncio.run(fgh())[0]))
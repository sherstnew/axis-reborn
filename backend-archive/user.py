from fastapi import APIRouter
from data.models import SquareBuild 
from handler import  users_per_week
from utils import analytics



router = APIRouter()

@router.post("/info")
async def create_SquareBuild(new_SquareBuild: SquareBuild):
    await new_SquareBuild.create()
    return await analytics(new_SquareBuild)


@router.get("/using_of_week")
async def analyticsW():
    count = await users_per_week(SquareBuild)
    return count





from datetime import datetime, timedelta
from beanie.operators import And



async def users_per_week(collection):
    current_time = datetime.now()
    counts = []

    for i in range(7):
        start_of_day = datetime(current_time.year, current_time.month, current_time.day - i)
        end_of_day = start_of_day + timedelta(days=1)
        count = await collection.find(And(collection.date >= start_of_day, collection.date < end_of_day)).count()
        counts.append(count)
    return counts



    
    
    
    
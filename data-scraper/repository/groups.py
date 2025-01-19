from database import select


async def get_level1_groups():
    return await select("SELECT * FROM level1_groups")

async def get_level2_groups():
    return await select("SELECT * FROM level2_groups")


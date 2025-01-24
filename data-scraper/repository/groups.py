from database import select
from models.Level2Group import Level2Group
from typing import List

async def get_level1_groups():
    return await select("SELECT * FROM level1_groups")

async def get_level2_groups():
    return await select("SELECT * FROM level2_groups")

async def get_level2_groups_by_product_table_id(product_table_id: int) -> List[Level2Group]:
    rows = await select("SELECT * FROM level2_groups WHERE product_table_id = ?", (product_table_id,))
    return [Level2Group(**row) for row in rows]

async def get_level2_groups_by_device(device: str, limit: int = 10) -> List[Level2Group]:
    rows = await select("SELECT * FROM level2_groups WHERE LOWER(device) = LOWER(?) LIMIT ?", (device, limit))
    return [Level2Group(**row) for row in rows]


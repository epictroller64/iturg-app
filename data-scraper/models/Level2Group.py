from pydantic import BaseModel


class Level2Group(BaseModel):
    id: int
    product_table_id: int
    device: str
    chip: str
    ram: str
    screen_size: str
    generation: str
    storage: str
    color: str
    status: str
    year: str
    watch_mm: str

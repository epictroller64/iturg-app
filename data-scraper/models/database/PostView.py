from pydantic import BaseModel


class PostView(BaseModel):
    id: int
    product_table_id: int
    view_count: int

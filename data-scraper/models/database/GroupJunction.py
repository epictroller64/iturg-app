from pydantic import BaseModel


class GroupJunction(BaseModel):
    """Define relationship between a feature and a product for easier querying"""
    id: int
    group_id: int
    product_table_id: int


    model_config = {
        "from_attributes": True
    }

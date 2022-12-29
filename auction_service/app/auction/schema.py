from pydantic import BaseModel
from typing import Optional


class AuctionModel(BaseModel):
    item_name: str
    start_time: str
    end_time: str
    start_price: int
    currency_string: str




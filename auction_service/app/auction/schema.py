from pydantic import BaseModel

class CreateAuction(BaseModel):
    item_name : str
    start_time : str

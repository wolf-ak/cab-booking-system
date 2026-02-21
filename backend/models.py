from pydantic import BaseModel

class BookingRequest(BaseModel):
    cab_id : int
    user_name : str
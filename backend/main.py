from fastapi import FastAPI

app = FastAPI(title="Cab Booking System API")

@app.get("/")
def health_check():
    return {"status": "API is running"}
cabs = [
    {"id": 1, "cab_number": "CAB-101", "is_available": True},
    {"id": 2, "cab_number": "CAB-102", "is_available": True},
    {"id": 3, "cab_number": "CAB-103", "is_available": True},
]

bookings = []

@app.get("/cabs")
def get_cabs():
    return cabs
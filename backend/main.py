from models import BookingRequest
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

@app.post("/bookings")
def create_booking(request: BookingRequest):

    cab = None

    # 1. Find the cab by ID
    for c in cabs:
        if c["id"] == request.cab_id:
            cab = c
            break

    # 2. If cab does not exist
    if cab is None:
        return {"error": "Cab not found"}

    # 3. Check for existing active booking (double booking prevention)
    for booking in bookings:
        if booking["cab_id"] == request.cab_id and booking["status"] == "active":
            return {"error": "Cab is already booked"}

    # 4. Create booking
    booking = {
        "id": len(bookings) + 1,
        "cab_id": request.cab_id,
        "user_name": request.user_name,
        "status": "active"
    }
    bookings.append(booking)

    # 5. Mark cab as unavailable
    cab["is_available"] = False

    return {
        "message": "Booking confirmed",
        "booking": booking
    }

@app.get("/bookings")
def get_bookings():
    return bookings

@app.delete("/bookings/{booking_id}")
def cancel_booking(booking_id: int):

    booking_to_cancel = None

    # 1. Find booking by ID
    for booking in bookings:
        if booking["id"] == booking_id:
            booking_to_cancel = booking
            break

    # 2. Booking not found
    if booking_to_cancel is None:
        return {"error": "Booking not found"}

    # 3. If already cancelled
    if booking_to_cancel["status"] == "cancelled":
        return {"message": "Booking already cancelled"}

    # 4. Cancel booking
    booking_to_cancel["status"] = "cancelled"

    # 5. Mark cab as available again
    for cab in cabs:
        if cab["id"] == booking_to_cancel["cab_id"]:
            cab["is_available"] = True
            break

    return {"message": "Booking cancelled successfully"}

@app.put("/bookings/{booking_id}/complete")
def complete_booking(booking_id: int):

    booking_to_complete = None

    # 1. Find booking
    for booking in bookings:
        if booking["id"] == booking_id:
            booking_to_complete = booking
            break

    # 2. Booking not found
    if booking_to_complete is None:
        return {"error": "Booking not found"}

    # 3. Only active bookings can be completed
    if booking_to_complete["status"] != "active":
        return {"error": "Only active bookings can be completed"}

    # 4. Mark booking as completed
    booking_to_complete["status"] = "completed"

    # 5. Free the cab
    for cab in cabs:
        if cab["id"] == booking_to_complete["cab_id"]:
            cab["is_available"] = True
            break

    return {"message": "Booking completed successfully"}
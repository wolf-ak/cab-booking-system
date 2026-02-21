import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("Cab Booking System")

st.write("Simple interface to view and book cabs")

st.subheader("Available Cabs")
if st.button("Load Cabs"):
    response = requests.get(f"{BASE_URL}/cabs")
    if response.status_code == 200:
        cabs = response.json()
        st.table(cabs)
    else:
        st.error("Failed to load cabs")

st.subheader("Book a Cab")

cab_id = st.number_input("Cab ID", min_value=1, step=1)
user_name = st.text_input("Your Name")

if st.button("Book Cab"):
    payload = {
        "cab_id": cab_id,
        "user_name": user_name
    }

    response = requests.post(f"{BASE_URL}/bookings", json=payload)

    if response.status_code == 200:
        data = response.json()
        if "error" in data:
            st.error(data["error"])
        else:
            st.success(data["message"])
            st.write(data["booking"])
    else:
        st.error("Booking request failed")

st.subheader("Booking History")

if st.button("Load Bookings"):
    response = requests.get(f"{BASE_URL}/bookings")
    if response.status_code == 200:
        bookings = response.json()
        if len(bookings) == 0:
            st.info("No bookings found")
        else:
            st.table(bookings)
    else:
        st.error("Failed to load booking history")

st.subheader("Cancel a Booking")

cancel_booking_id = st.number_input(
    "Booking ID to cancel",
    min_value=1,
    step=1
)

if st.button("Cancel Booking"):
    response = requests.delete(
        f"{BASE_URL}/bookings/{cancel_booking_id}"
    )

    if response.status_code == 200:
        data = response.json()
        if "error" in data:
            st.error(data["error"])
        else:
            st.success(data["message"])
    else:
        st.error("Failed to cancel booking")

st.subheader("Complete a Booking")

complete_booking_id = st.number_input(
    "Booking ID to complete",
    min_value=1,
    step=1,
    key="complete"
)

if st.button("Complete Booking"):
    response = requests.put(
        f"{BASE_URL}/bookings/{complete_booking_id}/complete"
    )

    if response.status_code == 200:
        data = response.json()
        if "error" in data:
            st.error(data["error"])
        else:
            st.success(data["message"])
    else:
        st.error("Failed to complete booking")
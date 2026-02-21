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
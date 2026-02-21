from fastapi import FastAPI

app = FastAPI(title="Cab Booking System API")

@app.get("/")
def health_check():
    return {"status": "API is running"}

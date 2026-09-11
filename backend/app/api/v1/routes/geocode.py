from fastapi import APIRouter, HTTPException
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

print("Loaded API key:", os.getenv("OPENCAGE_API_KEY"))

router = APIRouter(
    prefix="/geocode",
    tags=["Geocoding"]
)

@router.get("/address")
def geocode_address(address: str):
    OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")

    if not OPENCAGE_API_KEY:
        raise HTTPException(status_code=500, detail="Missing OpenCage API key")

    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        "q": address,
        "key": OPENCAGE_API_KEY,
        "limit": 1
    }

    headers = {
        "User-Agent": "tick-risk-backend/1.0 (contact: klake815@gmail.com)"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Geocoding service error: {response.status_code}")

    data = response.json()

    if not data["results"]:
        raise HTTPException(status_code=404, detail="Address not found")

    location = data["results"][0]["geometry"]

    return {
        "latitude": location["lat"],
        "longitude": location["lng"]
    }
def geocode_address_internal(address: str) -> dict:
    """
    Internal geocoding helper so other routes can call geocoding
    without making an HTTP request.
    Uses the same OpenCage logic as the public route.
    """
    OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")

    if not OPENCAGE_API_KEY:
        raise Exception("Missing OpenCage API key")

    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        "q": address,
        "key": OPENCAGE_API_KEY,
        "limit": 1
    }

    headers = {
        "User-Agent": "tick-risk-backend/1.0 (contact: klake815@gmail.com)"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Geocoding service error: {response.status_code}")

    data = response.json()

    if not data["results"]:
        raise Exception("Address not found")

    location = data["results"][0]["geometry"]

    return {
        "latitude": location["lat"],
        "longitude": location["lng"]
    }

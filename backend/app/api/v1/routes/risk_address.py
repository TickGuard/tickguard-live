from fastapi import APIRouter, HTTPException
from app.api.v1.routes.geocode import geocode_address_internal
from app.services.risk_engine import calculate_risk

router = APIRouter(
    prefix="/risk",
    tags=["Risk"]
)

@router.get("/address")
def risk_from_address(address: str, month: int):
    """
    Full workflow:
    1. Geocode the address → lat/long
    2. Pass coordinates + month into the risk engine
    3. Return final risk score
    """

    # Step 1 — Geocode internally
    try:
        geo = geocode_address_internal(address)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Geocoding failed: {str(e)}")

    latitude = geo["latitude"]
    longitude = geo["longitude"]

    # Step 2 — Risk engine
    try:
        score = calculate_risk(latitude=latitude, longitude=longitude, month=month)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk engine failed: {str(e)}")

    # Step 3 — Return final score
    return {
        "address": address,
        "latitude": latitude,
        "longitude": longitude,
        "month": month,
        "risk_score": score
    }

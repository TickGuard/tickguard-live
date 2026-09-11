from fastapi import APIRouter
from app.services.risk_engine import calculate_risk

router = APIRouter(
    prefix="/risk",
    tags=["Risk Assessment"]
)

@router.get("/calculate")
def calculate_risk_endpoint(latitude: float, longitude: float, month: int):
    result = calculate_risk(latitude, longitude, month)
    return {"risk_score": result}

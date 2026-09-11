from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# -----------------------------
# FASTAPI APP
# -----------------------------
app = FastAPI()

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}

# -----------------------------
# CORS (REQUIRED FOR LANDING PAGE)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow your local HTML file
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# ROUTERS
# -----------------------------
from app.api.v1.routes.risk import router as risk_router
from app.api.v1.routes.geocode import router as geocode_router
from app.api.v1.routes.risk_address import router as risk_address_router

app.include_router(risk_router, prefix="/api/v1")
app.include_router(geocode_router, prefix="/api/v1")
app.include_router(risk_address_router, prefix="/api/v1")

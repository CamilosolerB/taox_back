from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.infrastructure.adapters.into.http.users import router as users_router
from app.infrastructure.adapters.into.http.roles import router as roles_router
from app.infrastructure.adapters.into.http.companies import router as companies_router
from app.infrastructure.adapters.into.http.products import router as products_router
from app.infrastructure.adapters.into.http.auth import router as auth_router
from app.infrastructure.adapters.into.http.provider import router as provider_router
from app.infrastructure.adapters.into.http.location import router as location_router
from app.infrastructure.adapters.into.http.stock import router as stock_router
from app.infrastructure.adapters.into.http.client import router as client_router
from app.infrastructure.adapters.into.http.product_provider import router as product_provider_router
from app.infrastructure.adapters.into.http.processes import router as processes_router
from app.infrastructure.adapters.into.http.warehouses import router as warehouses_router
from app.infrastructure.adapters.into.http.product_movements import router as movements_router
from app.infrastructure.adapters.into.http.chemical_stocks import router as stocks_router
from app.infrastructure.adapters.into.http.stock_alerts import router as alerts_router
from app.infrastructure.adapters.into.http.dashboard import router as dashboard_router
from app.infrastructure.adapters.into.http.uploads import router as uploads_router
from app.core.middleware.security_headers import SecurityHeadersMiddleware, NoCacheMiddleware

app = FastAPI(title="TAOX API")

# Security headers (add first for proper order)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(NoCacheMiddleware)

# CORS - use environment variable for production
import os
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
# Ensure local static directory exists
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount /static/uploads to support Railway Persistent Volume with a local fallback
if os.path.exists("/static/uploads"):
    os.makedirs("/static/uploads/logos", exist_ok=True)
    os.makedirs("/static/uploads/fds", exist_ok=True)
    app.mount("/static/uploads", StaticFiles(directory="/static/uploads"), name="static_uploads")
else:
    os.makedirs("static/uploads/logos", exist_ok=True)
    os.makedirs("static/uploads/fds", exist_ok=True)
    app.mount("/static/uploads", StaticFiles(directory="static/uploads"), name="static_uploads")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(companies_router)
app.include_router(products_router)
app.include_router(provider_router)
app.include_router(location_router)
app.include_router(stock_router)
app.include_router(client_router)
app.include_router(product_provider_router)
# New inventory feature routers
app.include_router(processes_router)
app.include_router(warehouses_router)
app.include_router(movements_router)
app.include_router(stocks_router)
app.include_router(alerts_router)
app.include_router(dashboard_router)
app.include_router(uploads_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
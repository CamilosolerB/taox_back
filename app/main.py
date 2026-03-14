from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
from app.infrastructure.adapters.into.http.product_movements import router as movements_router
from app.infrastructure.adapters.into.http.chemical_stocks import router as stocks_router
from app.infrastructure.adapters.into.http.stock_alerts import router as alerts_router

app = FastAPI(title="TAOX API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
app.include_router(movements_router)
app.include_router(stocks_router)
app.include_router(alerts_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
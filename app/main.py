from fastapi import FastAPI
from app.infrastructure.adapters.into.http.users import router as users_router
from app.infrastructure.adapters.into.http.roles import router as roles_router
from app.infrastructure.adapters.into.http.companies import router as companies_router
from app.infrastructure.adapters.into.http.products import router as products_router

app = FastAPI(title="TAOX API")

app.include_router(users_router)
app.include_router(roles_router)
app.include_router(companies_router)
app.include_router(products_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
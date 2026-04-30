from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import hq, admin, customer

app = FastAPI(title="Table Order API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(hq.router)
app.include_router(admin.router)
app.include_router(customer.router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}

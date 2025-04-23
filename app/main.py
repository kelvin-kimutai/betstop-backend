from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import exclusions, telcos

app = FastAPI(title="BetStop API")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(exclusions.router)
app.include_router(telcos.router)

@app.get("/")
async def root():
    return {"message": "BetStop API"}
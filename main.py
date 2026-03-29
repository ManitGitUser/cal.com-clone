from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine
from models.base import Base
import models
from routes import event_types_router, availabilities_router, bookings_router
from seed import seed_database

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    Base.metadata.create_all(bind=engine)
    seed_database()
    yield

app = FastAPI(title="Booking API", lifespan=lifespan)

# Setup CORS Support
origins = [
    "http://localhost:5173", # standard Vite port
    "http://localhost:3000", # fallback
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(event_types_router)
app.include_router(availabilities_router)
app.include_router(bookings_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Booking API. Visit /docs for API documentation."}

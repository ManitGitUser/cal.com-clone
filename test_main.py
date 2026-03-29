from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest

from main import app
from database import get_db
from models.base import Base

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_event_type():
    response = client.post(
        "/event-types/",
        json={"name": "Consultation", "slug": "consultation", "duration": 30},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Consultation"
    assert data["slug"] == "consultation"
    assert data["duration"] == 30
    assert "id" in data
    return data["id"]
    
def test_create_event_type_invalid_duration():
    response = client.post(
        "/event-types/",
        json={"name": "Quick Chat", "slug": "quick-chat", "duration": -15},
    )
    assert response.status_code == 422

def test_create_availability():
    event_type_id = test_create_event_type()
    response = client.post(
        "/availabilities/",
        json={
            "start_time": "2024-05-01T10:00:00Z",
            "end_time": "2024-05-01T12:00:00Z",
            "event_type_id": event_type_id
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["event_type_id"] == event_type_id

def test_create_booking_and_prevent_double_booking():
    event_type_id = test_create_event_type()
    
    # First booking
    response = client.post(
        "/bookings/",
        json={
            "start_time": "2024-05-01T10:00:00Z",
            "end_time": "2024-05-01T10:30:00Z",
            "attendee_email": "test@example.com",
            "event_type_id": event_type_id
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["attendee_email"] == "test@example.com"
    
    # Second booking with same time and event type
    response = client.post(
        "/bookings/",
        json={
            "start_time": "2024-05-01T10:00:00Z",
            "end_time": "2024-05-01T10:30:00Z",
            "attendee_email": "another@example.com",
            "event_type_id": event_type_id
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Double booking is not allowed for this event at this time."

def test_get_available_slots():
    event_type_id = test_create_event_type()
    
    # Add availability
    client.post(
        "/availabilities/",
        json={
            "start_time": "2024-06-01T10:00:00Z",
            "end_time": "2024-06-01T12:00:00Z",
            "event_type_id": event_type_id
        },
    )
    
    # Add booking inside availability (10:00 - 10:30)
    client.post(
        "/bookings/",
        json={
            "start_time": "2024-06-01T10:00:00Z",
            "end_time": "2024-06-01T10:30:00Z",
            "attendee_email": "test@example.com",
            "event_type_id": event_type_id
        },
    )
    
    response = client.get(f"/event-types/{event_type_id}/slots?target_date=2024-06-01")
    assert response.status_code == 200
    slots = response.json()
    
    # 2 hours total availability = 4 slots (30 mins each). 1 booked -> 3 available.
    assert len(slots) == 3
    # Check that 10:00 is not in the list (first available should be 10:30)
    assert "2024-06-01T10:30:00Z" in slots[0]["start_time"]

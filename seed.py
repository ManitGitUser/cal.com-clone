from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import models
from database import SessionLocal

def seed_database():
    db: Session = SessionLocal()
    try:
        if db.query(models.EventType).count() > 0:
            print("Database already seeded.")
            return

        # Create Event Types
        event_30 = models.EventType(title="30 Min Meeting", slug="30-min-meeting", duration=30)
        event_60 = models.EventType(title="60 Min Interview", slug="60-min-interview", duration=60)
        
        db.add(event_30)
        db.add(event_60)
        db.commit()
        db.refresh(event_30)
        db.refresh(event_60)

        # Create Availability for the next 30 days (Mon-Fri, 9AM-5PM UTC)
        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        
        for i in range(30):
            current_day = today + timedelta(days=i)
            # Monday is 0, Sunday is 6
            if current_day.weekday() < 5: 
                start_avail = current_day.replace(hour=9, minute=0)
                end_avail = current_day.replace(hour=17, minute=0)
                
                db.add(models.Availability(event_type_id=event_30.id, start_time=start_avail, end_time=end_avail))
                db.add(models.Availability(event_type_id=event_60.id, start_time=start_avail, end_time=end_avail))
                
        db.commit()

        # Create Sample Bookings (one tomorrow, one day after tomorrow)
        tomorrow = today + timedelta(days=1)
        if tomorrow.weekday() >= 5: # If weekend, push to monday
            tomorrow += timedelta(days=2 if tomorrow.weekday() == 6 else 3)
            
        booking_1_start = tomorrow.replace(hour=10, minute=0)
        booking_1_end = booking_1_start + timedelta(minutes=30)
        
        booking_2_start = tomorrow.replace(hour=14, minute=0)
        booking_2_end = booking_2_start + timedelta(minutes=60)
        
        db.add(models.Booking(
            event_type_id=event_30.id, 
            start_time=booking_1_start, 
            end_time=booking_1_end,
            attendee_email="alice@example.com"
        ))
        
        db.add(models.Booking(
            event_type_id=event_60.id, 
            start_time=booking_2_start, 
            end_time=booking_2_end,
            attendee_email="bob@example.com"
        ))
        
        db.commit()
        print("Database seeded successfully with overlapping and baseline logic.")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from .models import Seat
from ..events.models import Event

router = APIRouter()

class SeatCreate(BaseModel):
    count: int   # Number of seats to generate

# -------------------------------------------
# Create seats for an event (Admin)
# -------------------------------------------
@router.post("/events/{event_id}/seats/create")
def create_seats(event_id: int, data: SeatCreate, db: Session = Depends(get_db)):

    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    created = []

    for i in range(1, data.count + 1):
        s = Seat(
            event_id=event_id,
            seat_number=f"S{i}",
            is_booked=False
        )
        db.add(s)
        created.append(s)

    db.commit()
    return {"message": f"{data.count} seats created", "event_id": event_id}

# -------------------------------------------
# Get all seats for an event
# -------------------------------------------
@router.get("/events/{event_id}/seats")
def list_seats(event_id: int, db: Session = Depends(get_db)):

    seats = db.query(Seat).filter(Seat.event_id == event_id).all()
    return seats

# -------------------------------------------
# Get only available seats
# -------------------------------------------
@router.get("/events/{event_id}/seats/available")
def get_available_seats(event_id: int, db: Session = Depends(get_db)):

    seats = db.query(Seat).filter(
        Seat.event_id == event_id,
        Seat.is_booked == False
    ).all()

    return seats

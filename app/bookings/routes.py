from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..seats.models import Seat
from .models import Booking

router = APIRouter()

class BookingCreate(BaseModel):
    user_id: int
    event_id: int
    seat_ids: list[int]   # MULTIPLE SEATS

@router.post("/")
def create_booking(data: BookingCreate, db: Session = Depends(get_db)):
    
    # Fetch all seats in the request
    seats = db.query(Seat).filter(Seat.id.in_(data.seat_ids)).all()

    # Validate ALL seats exist
    if len(seats) != len(data.seat_ids):
        raise HTTPException(400, "Some seats do not exist")

    # Validate all seats belong to the same event
    for seat in seats:
        if seat.event_id != data.event_id:
            raise HTTPException(400, "One or more seats do not belong to this event")

    # Validate seats are not booked
    for seat in seats:
        if seat.is_booked:
            raise HTTPException(400, f"Seat {seat.seat_number} already booked")

    # Mark seats as temporarily booked
    for seat in seats:
        seat.is_booked = True

    booking = Booking(
        user_id=data.user_id,
        event_id=data.event_id,
        seat_ids=",".join(map(str, data.seat_ids)),  # store seat IDs
        status="pending"
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return {
        "message": "Booking created",
        "booking_id": booking.id,
        "status": booking.status
    }

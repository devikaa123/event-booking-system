from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..bookings.models import Booking
from ..seats.models import Seat
from .stripe_utils import create_checkout_session

router = APIRouter()

class CheckoutRequest(BaseModel):
    booking_id: int


@router.post("/create-checkout-session")
def create_session(data: CheckoutRequest, db: Session = Depends(get_db)):

    booking = db.query(Booking).filter(Booking.id == data.booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.status == "paid":
        raise HTTPException(status_code=400, detail="Already paid")

    # Convert stored seat_ids string → list
    seat_ids = list(map(int, booking.seat_ids.split(",")))

    # Price calculation
    TICKET_PRICE = 500  # INR per seat
    total_amount = len(seat_ids) * TICKET_PRICE

    # Create Stripe Session
    session = create_checkout_session(
        amount=total_amount,
        booking_id=booking.id
    )

    return {
        "checkout_url": session.url,
        "total_amount": total_amount,
        "number_of_seats": len(seat_ids)
    }

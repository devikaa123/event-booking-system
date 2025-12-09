from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from ..database import get_db
from .models import Event

router = APIRouter()

# -----------------------------
# Pydantic Schema
# -----------------------------
class EventCreate(BaseModel):
    title: str
    description: str | None = None
    venue: str
    date: str   # user gives date as string

# -----------------------------
# ROUTES
# -----------------------------

# 1. Create Event
@router.post("/")
def create_event(event: EventCreate, db: Session = Depends(get_db)):

    # Convert string → datetime
    try:
        # Try full datetime
        date_obj = datetime.strptime(event.date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            # Try simple date
            date_obj = datetime.strptime(event.date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Use: YYYY-MM-DD or YYYY-MM-DD HH:MM:SS"
            )

    new_event = Event(
        title=event.title,
        description=event.description,
        venue=event.venue,
        date=date_obj
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return {"message": "Event created", "event_id": new_event.id}

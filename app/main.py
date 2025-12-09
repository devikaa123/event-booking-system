from fastapi import FastAPI
from .auth.routes import router as auth_router
from .events.routes import router as events_router
from .seats.routes import router as seats_router
from .bookings.routes import router as bookings_router
from .payments.routes import router as payments_router

app = FastAPI()

# Register routers only once
app.include_router(auth_router, prefix="/auth")
app.include_router(events_router, prefix="/events")
app.include_router(seats_router, prefix="/events")
app.include_router(bookings_router, prefix="/bookings")
app.include_router(payments_router, prefix="/payments")

@app.get("/")
def home():
    return {"message": "Event Booking System API is running"}

# Auto-create tables
from .database import Base, engine
from .auth.models import User
from .events.models import Event
from .seats.models import Seat
from .bookings.models import Booking

Base.metadata.create_all(bind=engine)

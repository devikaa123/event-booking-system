from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base
import datetime
from sqlalchemy.orm import relationship

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    venue = Column(String)
    date = Column(DateTime)

    seats = relationship("Seat", back_populates="event")

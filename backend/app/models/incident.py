from sqlalchemy import Column, Integer, String
from app.database.db import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    service = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    error_message = Column(String, nullable=False)
    endpoint = Column(String, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    severity = Column(String, nullable=True)
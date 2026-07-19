from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class ThreatReport(Base):
    __tablename__ = "threat_reports"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text)
    raw_data = Column(Text)
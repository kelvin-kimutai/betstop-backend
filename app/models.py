from sqlalchemy import Column, String, DateTime, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base
import enum
from sqlalchemy.sql import func

class ExclusionStatus(enum.Enum):
    active = "active"
    expired = "expired"

class PartnerType(enum.Enum):
    telco = "telco"
    betting_provider = "betting_provider"

class Exclusion(Base):
    __tablename__ = "exclusions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mobile_number = Column(String, unique=True, nullable=False)
    national_id_hash = Column(String, nullable=False)
    exclusion_start = Column(DateTime, nullable=False)
    exclusion_end = Column(DateTime, nullable=False)
    status = Column(Enum(ExclusionStatus), default=ExclusionStatus.active)

class ApiKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True)
    key_hash = Column(String, unique=True, nullable=False)
    partner_name = Column(String, nullable=False)
    partner_type = Column(Enum(PartnerType), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
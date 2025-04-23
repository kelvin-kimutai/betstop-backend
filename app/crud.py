from sqlalchemy.orm import Session
from app.models import Exclusion, ExclusionStatus
from app.schemas import ExclusionCreate
from datetime import datetime, timedelta
from hashlib import sha256
from sqlalchemy.exc import IntegrityError

def create_exclusion(db: Session, exclusion: ExclusionCreate):
    # Check if mobile number already exists
    existing_exclusion = db.query(Exclusion).filter(Exclusion.mobile_number == exclusion.mobile_number).first()
    if existing_exclusion:
        raise ValueError("Mobile number already registered for exclusion")

    # Mock telco verification
    national_id = "12345678"  # Replace with telco API call
    national_id_hash = sha256(national_id.encode()).hexdigest()

    # Calculate exclusion end date
    period_map = {"6m": 182, "1y": 365, "5y": 1825}
    exclusion_end = datetime.utcnow() + timedelta(days=period_map[exclusion.exclusion_period])

    db_exclusion = Exclusion(
        mobile_number=exclusion.mobile_number,
        national_id_hash=national_id_hash,
        exclusion_start=datetime.utcnow(),
        exclusion_end=exclusion_end,
        status=ExclusionStatus.active
    )
    try:
        db.add(db_exclusion)
        db.commit()
        db.refresh(db_exclusion)
        return db_exclusion
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Database error: unable to register exclusion")
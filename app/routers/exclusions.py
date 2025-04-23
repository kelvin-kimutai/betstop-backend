from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import ExclusionCreate, ExclusionResponse
from app.crud import create_exclusion
from app.database import get_db
from app.models import Exclusion
from app.dependencies import require_betting_provider
import re

router = APIRouter(prefix="/exclusions", tags=["exclusions"])

@router.post("/register-exclusion", response_model=ExclusionResponse)
async def register_exclusion(exclusion: ExclusionCreate, db: Session = Depends(get_db)):
    try:
        db_exclusion = create_exclusion(db, exclusion)
        return ExclusionResponse(
            exclusion_id=str(db_exclusion.id),
            mobile_number=db_exclusion.mobile_number,
            exclusion_start=db_exclusion.exclusion_start,
            exclusion_end=db_exclusion.exclusion_end,
            status=db_exclusion.status.value
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/check-exclusion", response_model=ExclusionResponse)
async def check_exclusion(mobile_number: str, db: Session = Depends(get_db)):
    if not re.match(r"^\+2547\d{8}$", mobile_number):
        raise HTTPException(status_code=400, detail="Invalid mobile number format")
    db_exclusion = db.query(Exclusion).filter(Exclusion.mobile_number == mobile_number).first()
    if not db_exclusion:
        raise HTTPException(status_code=404, detail="No exclusion found")
    return ExclusionResponse(
        exclusion_id=str(db_exclusion.id),
        mobile_number=db_exclusion.mobile_number,
        exclusion_start=db_exclusion.exclusion_start,
        exclusion_end=db_exclusion.exclusion_end,
        status=db_exclusion.status.value
    )

@router.get("/operators/check-exclusion", response_model=dict, dependencies=[Depends(require_betting_provider)])
async def operator_check_exclusion(mobile_number: str, db: Session = Depends(get_db)):
    if not re.match(r"^\+2547\d{8}$", mobile_number):
        raise HTTPException(status_code=400, detail="Invalid mobile number format")
    db_exclusion = db.query(Exclusion).filter(Exclusion.mobile_number == mobile_number).first()
    return {
        "excluded": bool(db_exclusion),
        "exclusion_end": db_exclusion.exclusion_end.isoformat() if db_exclusion else None
    }
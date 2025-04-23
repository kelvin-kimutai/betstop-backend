from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import require_telco
from pydantic import BaseModel

router = APIRouter(prefix="/telcos", tags=["telcos"])

class VerifyUserRequest(BaseModel):
    mobile_number: str
    national_id: str

class VerifyUserResponse(BaseModel):
    verified: bool
    details: dict

@router.post("/verify-user", response_model=VerifyUserResponse, dependencies=[Depends(require_telco)])
async def verify_user(request: VerifyUserRequest, db: Session = Depends(get_db)):
    # Mock Telco KYC (replace with real API call)
    if request.national_id == "12345678":
        return VerifyUserResponse(
            verified=True,
            details={"name": "John Doe", "id_number": request.national_id}
        )
    raise HTTPException(status_code=400, detail="Invalid national ID")
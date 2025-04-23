from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ApiKey, PartnerType
from app.utils import verify_api_key

async def get_api_key(authorization: str = Header(...), db: Session = Depends(get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    api_key = authorization.replace("Bearer ", "")
    db_api_keys = db.query(ApiKey).all()  # Fetch all keys
    for db_api_key in db_api_keys:
        if verify_api_key(api_key, db_api_key.key_hash):
            return db_api_key
    raise HTTPException(status_code=401, detail="Invalid API key")

def require_telco(api_key: ApiKey = Depends(get_api_key)):
    if api_key.partner_type != PartnerType.telco:
        raise HTTPException(status_code=403, detail="Telco access required")
    return api_key

def require_betting_provider(api_key: ApiKey = Depends(get_api_key)):
    if api_key.partner_type != PartnerType.betting_provider:
        raise HTTPException(status_code=403, detail="Betting provider access required")
    return api_key
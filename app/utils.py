import secrets
import bcrypt
from sqlalchemy.orm import Session
from app.models import ApiKey, PartnerType

def generate_api_key():
    return secrets.token_urlsafe(32)

def hash_api_key(api_key: str) -> str:
    return bcrypt.hashpw(api_key.encode(), bcrypt.gensalt()).decode()

def verify_api_key(api_key: str, key_hash: str) -> bool:
    return bcrypt.checkpw(api_key.encode(), key_hash.encode())

def create_api_key(db: Session, partner_name: str, partner_type: PartnerType) -> str:
    api_key = generate_api_key()
    key_hash = hash_api_key(api_key)
    db_api_key = ApiKey(
        key_hash=key_hash,
        partner_name=partner_name,
        partner_type=partner_type
    )
    db.add(db_api_key)
    db.commit()
    return api_key
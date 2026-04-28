from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from auth_utils import decode_token
from db import cursor

security = HTTPBearer()

def get_current_user(credentials=Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("user_id")

    cursor.execute(
        "SELECT id, name, email, role FROM users WHERE id=%s",
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "id": user[0],
        "name": user[1],
        "email": user[2],
        "role": user[3]
    }
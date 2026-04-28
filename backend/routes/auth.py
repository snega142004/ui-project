from fastapi import APIRouter, HTTPException
from db import cursor, conn
import bcrypt
from schemas import SignupModel, LoginModel
from auth_utils import create_token

router = APIRouter(prefix="/auth")

@router.post("/signup")
def signup(data: SignupModel):

    cursor.execute("SELECT id FROM users WHERE email=%s", (data.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()

    # 🔥 ALL USERS ADMIN (FINAL FIX)
    role = "admin"

    cursor.execute(
        """
        INSERT INTO users (name, email, password_hash, role)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """,
        (data.name, data.email, hashed, role)
    )

    user_id = cursor.fetchone()[0]
    conn.commit()

    token = create_token({
        "user_id": user_id,
        "role": role
    })

    return {
        "msg": "Signup success",
        "user_id": user_id,
        "access_token": token,
        "role": role
    }

@router.post("/login")
def login(data: LoginModel):

    cursor.execute(
        "SELECT id, password_hash, role FROM users WHERE email=%s",
        (data.email,)
    )
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_id, hashed, role = user

    if not bcrypt.checkpw(data.password.encode(), hashed.encode()):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_token({
        "user_id": user_id,
        "role": role
    })

    return {
        "msg": "Login success",
        "access_token": token,
        "role": role
    }
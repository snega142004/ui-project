from fastapi import APIRouter, Depends, HTTPException
from db import cursor, conn
from deps import get_current_user

router = APIRouter(prefix="/admin")

def check_admin(user):
    
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed")
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="not authorized")


@router.get("/users")
def get_users(user=Depends(get_current_user)):
    check_admin(user)


    cursor.execute("SELECT id, name, email, role FROM users")
    rows = cursor.fetchall()

    return [
        {"id": r[0], "name": r[1], "email": r[2], "role": r[3]}
        for r in rows
    ]


@router.get("/threads")
def get_threads(user=Depends(get_current_user)):
    check_admin(user)

    cursor.execute("SELECT * FROM threads")
    return cursor.fetchall()
    return rows


@router.get("/logs")
def get_logs(user=Depends(get_current_user)):
    check_admin(user)

    cursor.execute("SELECT * FROM query_logs")
    return cursor.fetchall()
    return rows

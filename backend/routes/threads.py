from fastapi import APIRouter, HTTPException, Depends
from db import cursor, conn
from deps import get_current_user

router = APIRouter(prefix="/threads")


# ✅ CREATE THREAD
@router.post("/")
def create_thread(title: str, user=Depends(get_current_user)):

    try:
        user_id = user["id"]

        cursor.execute(
            """
            INSERT INTO threads (user_id, title)
            VALUES (%s, %s)
            RETURNING id
            """,
            (user_id, title)
        )

        thread_id = cursor.fetchone()[0]
        conn.commit()

        return {"thread_id": thread_id}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ✅ GET THREADS (🔥 FIXED ROUTE)
@router.get("/")
def get_threads(user=Depends(get_current_user)):

    cursor.execute(
        """
        SELECT id, title, created_at
        FROM threads
        WHERE user_id=%s
        ORDER BY created_at DESC
        """,
        (user["id"],)
    )

    rows = cursor.fetchall()

    return [
        {
            "id": r[0],
            "title": r[1],
            "created_at": str(r[2])
        }
        for r in rows
    ]


# ✅ UPDATE TITLE
@router.put("/{thread_id}")
def update_thread(thread_id: int, data: dict):

    cursor.execute(
        "UPDATE threads SET title=%s WHERE id=%s",
        (data.get("title"), thread_id)
    )

    conn.commit()
    return {"msg": "updated"}


# ✅ DELETE THREAD
@router.delete("/{thread_id}")
def delete_thread(thread_id: int):

    cursor.execute(
        "DELETE FROM threads WHERE id=%s",
        (thread_id,)
    )

    conn.commit()
    return {"msg": "deleted"}
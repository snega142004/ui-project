from fastapi import APIRouter, HTTPException, Depends
from db import cursor, conn
from schemas import MessageCreate
from embedding import get_embedding
from routes.chat import detect_category
from deps import get_current_user

router = APIRouter(prefix="/messages")


def extract_section(text, category):

    text = text.replace("\n", " ")
    text = " ".join(text.split())

    sections = {
        "definition": ("1. Definition", "2."),
        "types": ("2. Types", "3."),
        "algorithms": ("3.", "4."),
        "applications": ("4.", "5."),
        "benefits": ("5.", "6."),
        "workflow": ("Workflow", "]")
    }

    if category not in sections:
        return None

    start_key, end_key = sections[category]

    start = text.lower().find(start_key.lower())
    if start == -1:
        return None

    end = text.lower().find(end_key.lower(), start + 1)

    if end == -1:
        return text[start:].strip()

    return text[start:end].strip()


# ✅ SEND MESSAGE
@router.post("/")
def send_message(data: MessageCreate, user=Depends(get_current_user)):

    try:
        thread_id = data.thread_id
        message = data.message
        user_id = user["id"]

        # check PDF
        cursor.execute(
            "SELECT id FROM documents WHERE user_id=%s LIMIT 1",
            (user_id,)
        )
        if not cursor.fetchone():
            return {"reply": "⚠️ Upload PDF first"}

        # save user msg
        cursor.execute(
            "INSERT INTO messages (thread_id, role, message) VALUES (%s,%s,%s)",
            (thread_id, "user", message)
        )

        category = detect_category(message)

        embedding = get_embedding(message)

        cursor.execute(
            """
            SELECT content
            FROM documents
            WHERE user_id=%s
            ORDER BY embedding <-> %s::vector
            LIMIT 1
            """,
            (user_id, str(embedding))
        )

        row = cursor.fetchone()

        if not row:
            reply = "No answer found"
        else:
            reply = extract_section(row[0], category) or "Not found"

        # save bot msg
        cursor.execute(
            "INSERT INTO messages (thread_id, role, message) VALUES (%s,%s,%s)",
            (thread_id, "assistant", reply)
        )

        conn.commit()
        return {"reply": reply}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ✅ GET MESSAGES
@router.get("/{thread_id}")
def get_messages(thread_id: int):

    cursor.execute(
        """
        SELECT role, message
        FROM messages
        WHERE thread_id=%s
        ORDER BY created_at
        """,
        (thread_id,)
    )

    rows = cursor.fetchall()

    return [
        {"role": r[0], "message": r[1]}
        for r in rows
    ]
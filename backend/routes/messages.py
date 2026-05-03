from fastapi import APIRouter, HTTPException, Depends
from db import cursor, conn
from schemas import MessageCreate
from embedding import get_embedding
from routes.chat import detect_category
from deps import get_current_user
from ai_model import ask_ai

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


@router.post("/")
def send_message(data: MessageCreate, user=Depends(get_current_user)):
    try:
        thread_id = data.thread_id
        message = data.message
        user_id = user["id"]

        # Save user message
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

        # PDF answer if available
        if row:
            pdf_answer = extract_section(row[0], category)

            if pdf_answer and len(pdf_answer) > 15:
                reply = pdf_answer
            else:
                reply = ask_ai(message)
        else:
            reply = ask_ai(message) or "No answer generated"

        # Save bot message
        cursor.execute(
            "INSERT INTO messages (thread_id, role, message) VALUES (%s,%s,%s)",
            (thread_id, "assistant", reply)
        )

        conn.commit()

        return {"reply": reply}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from deps import get_current_user   # 🔥 IMPORTANT
import psycopg2
from sentence_transformers import SentenceTransformer

router = APIRouter(prefix="/chat")

model = SentenceTransformer("all-MiniLM-L6-v2")

conn = psycopg2.connect(
    dbname="chat_db",
    user="postgres",
    password="2004",
    host="localhost",
    port="5434"
)

cursor = conn.cursor()


# ❌ REMOVE user_id
class AskRequest(BaseModel):
    question: str


# 🔥 CATEGORY DETECT
def detect_category(question):
    q = question.lower()

    if "define" in q or "what is" in q:
        return "definition"
    if "type" in q:
        return "types"
    if "algorithm" in q:
        return "algorithms"
    if "application" in q:
        return "applications"
    if "benefit" in q:
        return "benefits"
    if "workflow" in q:
        return "workflow"

    return "general"


# 🔥 SECTION EXTRACT
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


# 🔥 FINAL ASK API (TOKEN BASED)
@router.post("/ask")
def ask(data: AskRequest, user=Depends(get_current_user)):

    try:
        # ✅ user from token
        user_id = user["id"]

        question = data.question
        category = detect_category(question)

        query_embedding = model.encode(question).tolist()
        query_embedding_str = str(query_embedding)

        cursor.execute(
            """
            SELECT content
            FROM documents
            ORDER BY embedding <-> %s::vector
            LIMIT 1
            """,
            (query_embedding_str,)
        )

        row = cursor.fetchone()

        if not row:
            return {"answer": "No relevant data found"}

        full_text = row[0]

        answer = extract_section(full_text, category)

        if not answer:
            answer = "Answer not found in document"

        return {
            "user_id": user_id,   # optional debug
            "category": category,
            "answer": answer
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import APIRouter, UploadFile, File, Depends
import pdfplumber
from db import cursor, conn
from embedding import get_embedding
from deps import get_current_user

router = APIRouter(prefix="/upload")

@router.post("/")
async def upload_pdf(file: UploadFile = File(...), user=Depends(get_current_user)):

    user_id = user["id"]
    text = ""

    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"

    embedding = get_embedding(text)

    cursor.execute(
        "INSERT INTO documents (content, embedding, user_id) VALUES (%s,%s,%s)",
        (text, embedding, user_id)
    )

    conn.commit()

    return {"msg": "PDF uploaded"}
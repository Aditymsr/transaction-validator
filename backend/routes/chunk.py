from fastapi import APIRouter
import os

from utils.chunker import split_csv

router = APIRouter()

UPLOAD_FOLDER = "uploads"

@router.post("/split-file")
async def split_latest_file():

    files = [
        os.path.join(
            UPLOAD_FOLDER,
            f
        )
        for f in os.listdir(
            UPLOAD_FOLDER
        )
    ]

    if not files:

        return {
            "success": False,
            "message": "No uploaded file found"
        }

    latest_file = max(
        files,
        key=os.path.getctime
    )

    chunks = split_csv(
        latest_file,
        chunk_size=1000
    )

    return {
        "success": True,
        "total_chunks": len(chunks),
        "chunks": chunks
    }
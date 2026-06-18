from fastapi import APIRouter, UploadFile, File
import pandas as pd
import os
import uuid

router = APIRouter()

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

if os.path.exists(UPLOAD_FOLDER):
    if not os.path.isdir(UPLOAD_FOLDER):
        raise Exception(
            f"{UPLOAD_FOLDER} exists but is not a directory"
        )
else:
    os.makedirs(UPLOAD_FOLDER)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:

        if "." not in file.filename:
            return {
                "success": False,
                "message": "Invalid filename"
            }

        file_extension = file.filename.rsplit(".", 1)[1].lower()

        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        file_path = os.path.join(
            UPLOAD_FOLDER,
            unique_filename
        )

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        if file_extension == "csv":
            df = pd.read_csv(file_path)

        elif file_extension in ["xlsx", "xls"]:
            df = pd.read_excel(file_path)

        else:
            return {
                "success": False,
                "message": "Unsupported file type"
            }

        return {
            "success": True,
            "file_name": file.filename,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "preview": df.head(10).fillna("").to_dict(orient="records")
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
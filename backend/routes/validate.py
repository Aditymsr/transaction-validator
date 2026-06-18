from fastapi import APIRouter
import pandas as pd
import os
from fastapi.responses import FileResponse
import uuid
from validators.transaction_validator import validate_dataframe
import time

router = APIRouter()

UPLOAD_FOLDER = "uploads"

@router.post("/validate")
async def validate_latest_file():
    start_time = time.time()

    files = [
        os.path.join(UPLOAD_FOLDER, f)
        for f in os.listdir(UPLOAD_FOLDER)
    ]

    if not files:
        return {
            "success": False,
            "message": "No uploaded file found"
        }

    latest_file = max(files, key=os.path.getctime)

    if latest_file.endswith(".csv"):
        df = pd.read_csv(latest_file)
    else:
        df = pd.read_excel(latest_file)

    required_columns = [
        "OrderID",
        "CustomerName",
        "Country",
        "Phone",
        "Email",
        "OrderDate",
        "ProductID",
        "ProductName",
        "Quantity",
        "PaymentMode",
        "Amount"
    ]

    missing_columns = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:

        return {
            "success": False,
            "message": "Invalid dataset structure",
            "missing_columns": missing_columns
        }

    errors = validate_dataframe(df)
    report_rows = []

    for i in range(len(df)):

        row_number = i + 1

        matching_error = next(
            (
                err
                for err in errors
                if err["row"] == row_number
            ),
            None
        )

        if matching_error:

            report_rows.append({
                "Row": row_number,
                "Status": "Invalid",
                "Errors": "; ".join(
                    matching_error["errors"]
                )
            })

        else:

            report_rows.append({
                "Row": row_number,
                "Status": "Valid",
                "Errors": ""
            })

    invalid_rows = [
        error["row"] - 1
        for error in errors
    ]

    cleaned_df = df.drop(
        index=invalid_rows,
        errors="ignore"
    )

    total_records = len(df)

    invalid_records = len(errors)

    valid_records = total_records - invalid_records

    quality_score = round(
        (valid_records / total_records) * 100,
        2
    )
    if quality_score >= 95:

        grade = "A+"

    elif quality_score >= 90:

        grade = "A"

    elif quality_score >= 80:

        grade = "B"

    elif quality_score >= 70:

        grade = "C"

    else:

        grade = "D"
    os.makedirs("outputs", exist_ok=True)

    cleaned_filename = (
        f"cleaned_{uuid.uuid4().hex}.csv"
    )

    cleaned_path = os.path.join(
        "outputs",
        cleaned_filename
    )

    cleaned_df.to_csv(
        cleaned_path,
        index=False
    )
    os.makedirs(
        "reports",
        exist_ok=True
    )

    report_filename = (
        f"validation_report_{uuid.uuid4().hex}.csv"
    )

    report_path = os.path.join(
        "reports",
        report_filename
    )

    pd.DataFrame(
        report_rows
    ).to_csv(
        report_path,
        index=False
    )
    processing_time = round(
        time.time() - start_time,
        2
    )
    
    return {
    "success": True,
    "processing_time": processing_time,
    "total_records": total_records,
    "valid_records": valid_records,
    "invalid_records": invalid_records,
    "quality_score": quality_score,
    "grade": grade,
    "errors": errors,
    "cleaned_file": cleaned_filename,
    "report_file": report_filename
    }





@router.get(
    "/download-cleaned/{filename}",
    include_in_schema=False
)
async def download_cleaned_file(
    filename: str
):

    file_path = os.path.join(
        "outputs",
        filename
    )

    if not os.path.exists(file_path):
        return {
            "success": False,
            "message": "File not found"
        }

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/csv"
    )

@router.get("/download-latest-cleaned")
async def download_latest_cleaned():

    output_folder = "outputs"

    files = [
        os.path.join(output_folder, f)
        for f in os.listdir(output_folder)
        if f.endswith(".csv")
    ]

    if not files:
        return {
            "success": False,
            "message": "No cleaned files found"
        }

    latest_file = max(
        files,
        key=os.path.getctime
    )

    return FileResponse(
        latest_file,
        filename=os.path.basename(latest_file),
        media_type="text/csv"
    )

@router.get("/download-latest-report")
async def download_latest_report():

    report_folder = "reports"

    files = [
        os.path.join(report_folder, f)
        for f in os.listdir(report_folder)
        if f.endswith(".csv")
    ]

    if not files:
        return {
            "success": False,
            "message": "No report found"
        }

    latest_file = max(
        files,
        key=os.path.getctime
    )

    return FileResponse(
        latest_file,
        filename=os.path.basename(latest_file),
        media_type="text/csv"
    )
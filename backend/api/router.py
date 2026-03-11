from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from pydantic import EmailStr
import pandas as pd
import io

from services.ai_service import generate_sales_summary
from services.email_service import send_email
from core.security import verify_api_key

router = APIRouter()

def process_and_send(file_content: bytes, filename: str, email: str) -> dict:
    # Determine file type and parse with pandas
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(file_content))
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(file_content))
        else:
            return {"success": False, "message": "Invalid file type."}
            
        data_preview = df.head(50).to_csv(index=False)
        total_rows = len(df)
        columns = ", ".join(df.columns)
        summary_stats = df.describe(include="all").to_string()
        
        prompt_data = f"File contained {total_rows} rows. Columns: {columns}.\nStats:\n{summary_stats}\nPreview:\n{data_preview}"
        
        print("Generating AI summary...")
        summary_text = generate_sales_summary(prompt_data)
        
        if "An error occurred" in summary_text:
            return {"success": False, "message": summary_text}
            
        print("Sending email...")
        email_success, email_msg = send_email(email, "Sales Data AI Summary", summary_text)
        
        return {
            "success": email_success, 
            "message": email_msg,
            "summary": summary_text
        }
    except Exception as e:
        print(f"Error in processing task: {e}")
        return {"success": False, "message": f"Processing error: {str(e)}"}

@router.post("/upload", status_code=200)
def upload_sales_data(
    file: UploadFile = File(...),
    email: EmailStr = Form(...),
    api_key: str = Depends(verify_api_key)
):
    """
    Upload a sales data file (.csv or .xlsx) and an email address.
    The system will parse the file, generate an AI summary via Gemini,
    and send the results to the requested email.
    """
    if not (file.filename.endswith(".csv") or file.filename.endswith(".xlsx")):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload .csv or .xlsx.")
        
    file_content = file.file.read()
    
    # Process synchronously to return immediate status
    result = process_and_send(file_content, file.filename, email)
    
    if not result["success"]:
        # We can still return 200 with an error payload so the frontend can display it nicely
        return {"status": "warning", "message": result["message"], "summary": result.get("summary", "")}
    
    return {"status": "success", "message": result["message"], "summary": result["summary"]}

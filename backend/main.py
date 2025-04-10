# backend/main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from minio import Minio
import uuid
import requests
import os

app = FastAPI()

# Allow CORS from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure MinIO client
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "csv-files")

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # Set to True if using TLS
)

# Ensure bucket exists
if not minio_client.bucket_exists(MINIO_BUCKET):
    minio_client.make_bucket(MINIO_BUCKET)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        file_id = f"{uuid.uuid4()}-{file.filename}"
        minio_client.put_object(
            MINIO_BUCKET, file_id, data=bytes(file_content),
            length=len(file_content), content_type=file.content_type
        )
        return {"message": "File uploaded successfully", "file_id": file_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(question: str = Form(...), file_id: str = Form(...)):
    # Retrieve CSV file content from MinIO if needed for context.
    try:
        response = minio_client.get_object(MINIO_BUCKET, file_id)
        csv_data = response.read().decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=404, detail="File not found in storage.")

    # Construct the prompt using CSV content.
    prompt = (
        f"Here is the CSV data:\n{csv_data}\n\n"
        f"Based on the attached data, answer the following question:\n{question}"
    )

    # Call the Ollama LLM API; update OLLAMA_API_URL as needed.
    try:
        ollama_api_url = os.getenv("OLLAMA_API_URL", "http://ollama:5000/api")
        llm_response = requests.post(ollama_api_url, json={"prompt": prompt})
        llm_response.raise_for_status()
        answer = llm_response.json().get("answer", "No answer returned")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM API call failed: {str(e)}")

    return {"question": question, "answer": answer}

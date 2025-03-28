# app/app.py
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from app.services.s3_service import upload_to_s3, delete_from_s3
from config import Config

app = FastAPI()

@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    mime_type: str = Query(None, description="MIME type del archivo"),
    bucket: str = Query(Config.OVH_BUCKET_NAME, description="Nombre del bucket"),  # Usar el bucket desde Config
    filename: str = Query(None, description="Nombre del archivo en el almacenamiento")
):
    try:
        file_url = await upload_to_s3(file, mime_type, bucket, filename)
        return JSONResponse(content={"file_url": file_url}, status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete/")
async def delete_file(
    bucket: str = Query(Config.OVH_BUCKET_NAME, description="Nombre del bucket"),  # Usar el bucket desde Config
    filename: str = Query(..., description="Nombre del archivo en el almacenamiento")
):
    try:
        response = await delete_from_s3(bucket, filename)
        return JSONResponse(content=response, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

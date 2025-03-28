from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.config import Config

app = FastAPI()

ACCESS_KEY = "e85686a635a6416fa784ee60dd93bdff"
SECRET_KEY = "a1a0f6827d0740b2a13dfc88a529facf"
ENDPOINT = "https://s3.de.io.cloud.ovh.net/"

s3_config = Config(
    signature_version="s3v4",
    request_checksum_calculation="when_required",
    response_checksum_validation="when_required"
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    endpoint_url=ENDPOINT,
    config=s3_config
)

@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    mime_type: str = Query(None, description="MIME type del archivo"),
    bucket: str = Query("retail-images", description="Nombre del bucket"),
    filename: str = Query(None, description="Nombre del archivo en el almacenamiento")
):
    try:
        filename = filename or file.filename

        unique_filename = f"fernando-{filename}"

        mime_type = mime_type or file.content_type

        file_content = file.file.read()

        s3_client.put_object(
            Bucket=bucket,
            Key=unique_filename,
            Body=file_content,
            ContentType=mime_type,
            ACL="public-read",
        )

        file_url = f"https://{bucket}.s3.de.io.cloud.ovh.net/{unique_filename}"

        return JSONResponse(content={"file_url": file_url}, status_code=201)

    except NoCredentialsError:
        raise HTTPException(status_code=401, detail="Credenciales de OVH Object Storage no válidas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
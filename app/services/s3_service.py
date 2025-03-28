# app/services/s3_service.py
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.config import Config

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

async def upload_to_s3(file, mime_type, bucket, filename):
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
        return file_url

    except NoCredentialsError:
        raise Exception("Credenciales de OVH Object Storage no válidas")

async def delete_from_s3(bucket, filename):
    try:
        response = s3_client.delete_object(
            Bucket=bucket,
            Key=filename
        )
        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 204:
            return {"message": "File deleted successfully"}
        else:
            raise Exception("Failed to delete file from S3")
    except NoCredentialsError:
        raise Exception("Credenciales de OVH Object Storage no válidas")
    except Exception as e:
        raise Exception(f"Error deleting file: {str(e)}")

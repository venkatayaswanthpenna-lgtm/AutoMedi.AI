import os
import boto3
import logging
from botocore.exceptions import NoCredentialsError, ClientError
from app.core.config import settings
from uuid import uuid4

logger = logging.getLogger(__name__)

# Try to initialize the S3 client if keys are provided
s3_client = None
if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY and settings.AWS_S3_BUCKET_NAME:
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
    except Exception as e:
        logger.error(f"Failed to initialize S3 client: {e}")

async def upload_file(file_obj, filename: str, content_type: str = None) -> str:
    """
    Uploads a file to S3 and returns the public URL.
    Falls back to local storage if AWS credentials are not configured.
    """
    unique_filename = f"{uuid4()}_{filename}"
    
    # 1. Fallback to Local Storage if no S3 configured
    if not s3_client:
        logger.warning("AWS S3 not configured. Saving file locally as fallback.")
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        local_path = os.path.join(upload_dir, unique_filename)
        
        with open(local_path, "wb") as f:
            f.write(file_obj.read())
            
        return local_path
        
    # 2. Upload to S3
    try:
        bucket = settings.AWS_S3_BUCKET_NAME
        extra_args = {}
        if content_type:
            extra_args['ContentType'] = content_type
            
        # Optional: set ACL to public-read if your bucket allows it
        # extra_args['ACL'] = 'public-read'
        
        s3_client.upload_fileobj(
            file_obj,
            bucket,
            unique_filename,
            ExtraArgs=extra_args
        )
        
        s3_url = f"https://{bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{unique_filename}"
        return s3_url
        
    except (NoCredentialsError, ClientError) as e:
        logger.error(f"S3 Upload failed: {e}. Falling back to local storage.")
        
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        local_path = os.path.join(upload_dir, unique_filename)
        
        # We need to seek back to 0 since upload_fileobj might have read it
        file_obj.seek(0)
        with open(local_path, "wb") as f:
            f.write(file_obj.read())
            
        return local_path

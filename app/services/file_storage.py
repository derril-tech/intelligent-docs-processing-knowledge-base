import os
import aiofiles
from fastapi import UploadFile
from typing import Optional
import structlog
from app.core.config import settings

logger = structlog.get_logger()

class FileStorageService:
    """Service for handling file storage operations"""
    
    def __init__(self):
        self.storage_type = settings.STORAGE_TYPE
        self.local_storage_path = settings.LOCAL_STORAGE_PATH
        
        # Ensure local storage directory exists
        if self.storage_type == "local":
            os.makedirs(self.local_storage_path, exist_ok=True)
    
    async def save_file(self, file: UploadFile, filename: str) -> str:
        """Save uploaded file to storage"""
        try:
            if self.storage_type == "local":
                return await self._save_to_local(file, filename)
            elif self.storage_type == "s3":
                return await self._save_to_s3(file, filename)
            elif self.storage_type == "gcs":
                return await self._save_to_gcs(file, filename)
            else:
                raise ValueError(f"Unsupported storage type: {self.storage_type}")
                
        except Exception as e:
            logger.error("Failed to save file", filename=filename, error=str(e))
            raise
    
    async def _save_to_local(self, file: UploadFile, filename: str) -> str:
        """Save file to local filesystem"""
        file_path = os.path.join(self.local_storage_path, filename)
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        logger.info("File saved to local storage", filename=filename, path=file_path)
        return file_path
    
    async def _save_to_s3(self, file: UploadFile, filename: str) -> str:
        """Save file to AWS S3"""
        try:
            import boto3
            from botocore.exceptions import ClientError
            
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            
            content = await file.read()
            s3_client.put_object(
                Bucket=settings.S3_BUCKET_NAME,
                Key=filename,
                Body=content,
                ContentType=file.content_type
            )
            
            file_path = f"s3://{settings.S3_BUCKET_NAME}/{filename}"
            logger.info("File saved to S3", filename=filename, path=file_path)
            return file_path
            
        except ImportError:
            raise ValueError("boto3 not installed for S3 storage")
        except ClientError as e:
            logger.error("S3 upload failed", filename=filename, error=str(e))
            raise
    
    async def _save_to_gcs(self, file: UploadFile, filename: str) -> str:
        """Save file to Google Cloud Storage"""
        try:
            from google.cloud import storage
            
            storage_client = storage.Client()
            bucket = storage_client.bucket(settings.S3_BUCKET_NAME)  # Reusing S3 bucket name for GCS
            blob = bucket.blob(filename)
            
            content = await file.read()
            blob.upload_from_string(content, content_type=file.content_type)
            
            file_path = f"gcs://{settings.S3_BUCKET_NAME}/{filename}"
            logger.info("File saved to GCS", filename=filename, path=file_path)
            return file_path
            
        except ImportError:
            raise ValueError("google-cloud-storage not installed for GCS storage")
        except Exception as e:
            logger.error("GCS upload failed", filename=filename, error=str(e))
            raise
    
    async def delete_file(self, file_path: str) -> bool:
        """Delete file from storage"""
        try:
            if file_path.startswith("s3://"):
                return await self._delete_from_s3(file_path)
            elif file_path.startswith("gcs://"):
                return await self._delete_from_gcs(file_path)
            else:
                return await self._delete_from_local(file_path)
                
        except Exception as e:
            logger.error("Failed to delete file", file_path=file_path, error=str(e))
            return False
    
    async def _delete_from_local(self, file_path: str) -> bool:
        """Delete file from local filesystem"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info("File deleted from local storage", path=file_path)
                return True
            return False
        except Exception as e:
            logger.error("Local file deletion failed", path=file_path, error=str(e))
            return False
    
    async def _delete_from_s3(self, file_path: str) -> bool:
        """Delete file from S3"""
        try:
            import boto3
            from botocore.exceptions import ClientError
            
            # Extract bucket and key from s3://bucket/key format
            path_parts = file_path.replace("s3://", "").split("/", 1)
            bucket_name = path_parts[0]
            key = path_parts[1] if len(path_parts) > 1 else ""
            
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            
            s3_client.delete_object(Bucket=bucket_name, Key=key)
            logger.info("File deleted from S3", path=file_path)
            return True
            
        except Exception as e:
            logger.error("S3 file deletion failed", path=file_path, error=str(e))
            return False
    
    async def _delete_from_gcs(self, file_path: str) -> bool:
        """Delete file from GCS"""
        try:
            from google.cloud import storage
            
            # Extract bucket and blob from gcs://bucket/key format
            path_parts = file_path.replace("gcs://", "").split("/", 1)
            bucket_name = path_parts[0]
            blob_name = path_parts[1] if len(path_parts) > 1 else ""
            
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.delete()
            
            logger.info("File deleted from GCS", path=file_path)
            return True
            
        except Exception as e:
            logger.error("GCS file deletion failed", path=file_path, error=str(e))
            return False
    
    async def get_file_url(self, file_path: str, expires_in: int = 3600) -> Optional[str]:
        """Get presigned URL for file access"""
        try:
            if file_path.startswith("s3://"):
                return await self._get_s3_presigned_url(file_path, expires_in)
            elif file_path.startswith("gcs://"):
                return await self._get_gcs_signed_url(file_path, expires_in)
            else:
                return file_path  # Local files return the path directly
                
        except Exception as e:
            logger.error("Failed to get file URL", file_path=file_path, error=str(e))
            return None
    
    async def _get_s3_presigned_url(self, file_path: str, expires_in: int) -> str:
        """Get S3 presigned URL"""
        import boto3
        
        path_parts = file_path.replace("s3://", "").split("/", 1)
        bucket_name = path_parts[0]
        key = path_parts[1] if len(path_parts) > 1 else ""
        
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': key},
            ExpiresIn=expires_in
        )
        
        return url
    
    async def _get_gcs_signed_url(self, file_path: str, expires_in: int) -> str:
        """Get GCS signed URL"""
        from google.cloud import storage
        
        path_parts = file_path.replace("gcs://", "").split("/", 1)
        bucket_name = path_parts[0]
        blob_name = path_parts[1] if len(path_parts) > 1 else ""
        
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        url = blob.generate_signed_url(
            version="v4",
            expiration=expires_in,
            method="GET"
        )
        
        return url

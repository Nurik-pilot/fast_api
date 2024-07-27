from datetime import datetime, UTC
from typing import BinaryIO
from uuid import uuid4

from boto3 import resource, client
from botocore.config import Config
from pydantic import (
    BaseModel, AnyHttpUrl, Field,
)


class S3Request(BaseModel):
    class Fields(BaseModel):
        key: str
        content_type: str = Field(
            alias='Content-Type',
        )
        aws_access_key_id: str = Field(
            alias='AWSAccessKeyId',
        )
        policy: str
        signature: str

    url: AnyHttpUrl
    fields: Fields


class S3Client:
    def __init__(
        self,
        endpoint_url: str | None,
        access_key_id: str,
        secret_access_key: str,
        s3_bucket: str,
    ) -> None:
        """
        Generic s3 client

        :param endpoint_url:
        :param access_key_id:
        :param secret_access_key:
        :param s3_bucket:
        """
        config = Config(
            retries={
                'max_attempts': 16,
                'mode': 'standard',
            },
        )
        self.client = client(
            service_name='s3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            config=config,
        )
        self.bucket = resource(
            service_name='s3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            config=config,
        ).Bucket(name=s3_bucket)

    def bucket_exists(self) -> bool:
        created_at = self.bucket.creation_date
        return isinstance(
            created_at, datetime,
        )

    def object_exists(self, key: str) -> bool:
        objects = self.bucket.objects
        objects = objects.filter(
            Prefix=key, MaxKeys=1,
        )
        return len(tuple(objects)) >= 1

    def put(
        self, folder: str,
        filename: str,
        data: BinaryIO,
    ) -> str:
        now = datetime.now(tz=UTC)
        created_at: str = now.strftime(
            format=f'{folder}/%Y/%m/%d',
        )
        prefix = uuid4()
        saved = f'{prefix}_{filename}'
        key = '/'.join(
            (
                created_at, saved,
            ),
        )
        obj = self.bucket.Object(
            key=key,
        )
        obj.put(Body=data)
        return obj.key

    def request_for(
        self, key: str,
        content_type: str,
    ) -> S3Request:
        obj = self.client.generate_presigned_post(
            Bucket=self.bucket.name,
            Key=key, Fields={
                'Content-Type': content_type,
            }, ExpiresIn=3600,
        )
        return S3Request.model_validate(
            obj=obj,
        )

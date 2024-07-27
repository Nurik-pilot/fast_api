from datetime import datetime, UTC
from pathlib import Path

from requests import Session, Response

from common.clients import S3Request, S3Client
from core.settings import Settings


def test_s3_client(
    test_settings: Settings,
) -> None:
    _ = test_settings
    client = S3Client(
        endpoint_url=_.s3_endpoint_url,
        access_key_id=_.s3_access_key_id,
        secret_access_key=_.s3_secret_access_key,
        s3_bucket=_.s3_bucket_name,
    )
    key: str
    prefix = 'files'
    filename = 'sample.jpg'
    filepath = '/'.join(
        (
            '/src', 'common',
            'tests', 'data',
            filename,
        ),
    )
    path = Path(filepath)
    with path.open(mode='rb') as file:
        key = client.put(
            folder=prefix,
            filename=filename,
            data=file,
        )
    assert isinstance(key, str) is True
    now = datetime.now(tz=UTC)
    created_at: str = now.strftime(
        format=f'{prefix}/%Y/%m/%d',
    )
    assert created_at in key
    assert client.object_exists(
        key=key,
    ) is True


def test_s3_client_bucket_exists(
    test_settings: Settings,
) -> None:
    _ = test_settings
    client = S3Client(
        endpoint_url=_.s3_endpoint_url,
        access_key_id=_.s3_access_key_id,
        secret_access_key=_.s3_secret_access_key,
        s3_bucket=_.s3_bucket_name,
    )
    assert client.bucket_exists() is True


def test_s3_client_pre_signed_post(
    test_settings: Settings,
) -> None:
    filename = 'pre_signed_sample.jpg'
    key = f'files/2022/06/01/{filename}'
    _ = test_settings
    client = S3Client(
        endpoint_url=_.s3_endpoint_url,
        access_key_id=_.s3_access_key_id,
        secret_access_key=_.s3_secret_access_key,
        s3_bucket=_.s3_bucket_name,
    )
    s3_request: S3Request = client.request_for(
        key=key, content_type='image/jpg',
    )
    session: Session
    file_path = '/'.join(
        (
            '/src', 'common',
            'tests', 'data',
            'sample.jpg',
        ),
    )
    path = Path(file_path)
    with (
        path.open(mode='rb') as file,
        Session() as session,
    ):
        files = {'file': file}
        response: Response = session.post(
            url=str(s3_request.url),
            data=s3_request.fields.model_dump(
                by_alias=True,
            ),
            files=files,
        )
        assert response.status_code == 403

from common.clients import RedisClient
from core.settings import Settings


def test_redis_client(
    test_settings: Settings,
) -> None:
    key: str = 'key'
    value: str = 'value'
    redis_client = RedisClient(
        redis_url=test_settings.redis_url,
    )
    redis_client.put(key=key, value=value)
    assert redis_client.get(
        key=key,
    ) == value

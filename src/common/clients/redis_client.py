from redis import Redis


class RedisClient:
    def __init__(self, redis_url: str) -> None:
        """
        Generic redis client

        :param redis_url:
        """
        super().__init__()
        self.resource = Redis.from_url(
            url=redis_url,
            decode_responses=True,
            retry_on_timeout=True,
        )

    def put(self, key: str, value: str) -> None:
        self.resource.set(name=key, value=value)

    def flush_db(self) -> None:
        self.resource.flushdb(asynchronous=False)

    def get(
        self, key: str, default: str | None = None,
    ) -> str | None:
        value = self.resource.get(name=key)
        return default if value is None else value

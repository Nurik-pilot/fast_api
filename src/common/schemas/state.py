from pydantic import BaseModel


class StateResponse(BaseModel):
    database_works: bool
    cache_works: bool
    broker_works: bool

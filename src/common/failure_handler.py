from fastapi import HTTPException

from .schemas import (
    GenericError, ClientError,
    ResourceNotFound,
)


class FailureHandler:
    status_code: int = 500
    detail: str
    status_codes: dict[
        type[GenericError], int,
    ]

    def __init__(self) -> None:
        super().__init__()
        self.detail = 'Internal Server Error.'
        self.status_codes = {
            ResourceNotFound: 404,
            ClientError: 422,
        }

    def handle(
        self, failure: GenericError,
    ) -> None:
        failure_type = type(failure)
        status_code = self.status_codes.get(
            failure_type, self.status_code,
        )
        detail = (
            self.detail
            if failure.detail is None
            else failure.detail
        )
        raise HTTPException(
            status_code=status_code,
            detail=detail,
        )

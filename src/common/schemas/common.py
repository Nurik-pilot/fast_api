from dataclasses import dataclass


@dataclass
class GenericError:
    detail: str


@dataclass
class ClientError(GenericError):
    pass


@dataclass
class ResourceNotFound(ClientError):
    pass

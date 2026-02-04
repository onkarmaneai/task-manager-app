from dataclasses import dataclass


@dataclass
class APIError(Exception):
    code: str
    message: str
    status_code: int = 400


class AuthenticationError(APIError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(code=code, message=message, status_code=401)


class NotFoundError(APIError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(code=code, message=message, status_code=404)


class ConflictError(APIError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(code=code, message=message, status_code=409)

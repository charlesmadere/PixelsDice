from typing import Final


class GenericNetworkException(Exception):

    def __init__(
        self,
        message: str,
        statusCode: int | None = None,
    ):
        super().__init__(message)

        if statusCode is not None and not isinstance(statusCode, int):
            raise TypeError(f'statusCode argument is malformed: \"{statusCode}\"')

        self.__statusCode: Final[int | None] = statusCode

    @property
    def statusCode(self) -> int | None:
        return self.__statusCode


class NetworkResponseIsClosedException(Exception):

    def __init__(self, message: str):
        super().__init__(message)

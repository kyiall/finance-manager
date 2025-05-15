class CustomException(Exception):
    def __init__(self, name: str, status_code: int = 500):
        self.name = name
        self.status_code = status_code


class CustomError(CustomException):
    pass

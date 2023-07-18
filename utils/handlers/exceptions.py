class CMDException(Exception):
    message: str

    def __init__(self, message: str | None = None):
        self.message = message or self.message


class TestCMDExpcetion(CMDException):
    EXCEPTION_MESSAGE: str = 'Это текст тестовой ошибки'

    def __init__(self):
        super().__init__(message=self.EXCEPTION_MESSAGE)

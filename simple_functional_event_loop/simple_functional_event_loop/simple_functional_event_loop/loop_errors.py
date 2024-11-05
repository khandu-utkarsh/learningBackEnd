class IOError(Exception):
    def __init__(self, message, errorno, errorcode):
        super().__init__(message)
        self.errorno = errorno
        self.errorcode = errorcode

    def __str__(self):
        return super().__str__() + f' (error {self.errorno} {self.errorcode})'


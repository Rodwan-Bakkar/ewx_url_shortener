

class ResponseError(Exception):
    def __init__(self, msg, code):
        self.code = code
        self.msg = msg


class URLNotPresentError(ResponseError):
    pass


class InvalidShortCodeError(ResponseError):
    pass


class ShortCodeAlreadyInUseError(ResponseError):
    pass


class ShortCodeNotFoundError(ResponseError):
    pass

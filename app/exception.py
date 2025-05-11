class UserNotFoundException(Exception):
    detail = "User not found"


class UserNotCorrectPasswordException(Exception):
    detail = "User not correct password"


class TokenExpired(Exception):
    detail = "Token expired"


class TokenNotCorrect(Exception):
    detail = "Token not correct"


class UserNotFound(Exception):
    detail = "User was not found"


class PostNotFound(Exception):
    detail = "Post was not found"

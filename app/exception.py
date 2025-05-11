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


class WeatherUnaveliable(Exception):
    detail = "Weather service unavailable"


class UserAlreaydeExist(Exception):
    detail = "Пользователь с таким email уже существует"

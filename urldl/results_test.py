from returns.result import Result, Success, Failure


def divide(first: float, second: float) -> Result[float, ZeroDivisionError]:
    try:
        return Success(first / second)
        # => error: incompatible type "str"; expected "float"
    except ZeroDivisionError as exc:
        return Failure(ZeroDivisionError)
        # => error: incompatible type "int"; expected "ZeroDivisionError"

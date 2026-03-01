from functools import wraps
from datetime import datetime
from typing import Optional, Callable, Any


def _write(message: str, filename: Optional[str]) -> None:
    """Write log message to file or print to console.

    Args:
        message: строка сообщения для логирования
        filename: имя файла для записи, если None — вывод в консоль
    """
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)


def log(_func: Optional[Callable] = None, *, filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования вызовов функций.

    Логирует время вызова, имя функции, переданные аргументы, результат или информацию об ошибке.

    Можно применять как `@log` или `@log()` или `@log(filename='file.txt')`.

    Args:
        _func: функция, если декоратор применён без скобок
        filename: имя файла для записи логов. Если None — вывод в консоль.

    Returns:
        Декоратор-функция.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            ts = datetime.now().isoformat()
            _write(f"[{ts}] CALL: {func.__name__} args={args} kwargs={kwargs}", filename)
            try:
                result = func(*args, **kwargs)
                ts_ret = datetime.now().isoformat()
                _write(f"[{ts_ret}] RETURN: {func.__name__} -> {result!r}", filename)
                return result
            except Exception as exc:  # noqa: BLE001 - we re-raise
                ts_err = datetime.now().isoformat()
                _write(
                    f"[{ts_err}] ERROR: {func.__name__} {type(exc).__name__}: {exc} args={args} kwargs={kwargs}",
                    filename,
                )
                raise

        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)

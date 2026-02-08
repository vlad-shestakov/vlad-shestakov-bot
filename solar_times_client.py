"""Обёртка вызова CLI модуля solar-times (subprocess) для бота."""

import base64
import datetime
import json
import os
import subprocess
import sys

# Путь к модулю solar-times относительно корня бота
_BOT_ROOT = os.path.dirname(os.path.abspath(__file__))
MODULE_NAME = "solar-times"
MODULE_DIR = os.path.join(_BOT_ROOT, "modules", MODULE_NAME)
MODULE_CLI = os.path.join(MODULE_DIR, "cli.py")

# Таймауты (секунды)
SOLAR_NOON_TIMEOUT = 30
SOLAR_TIMES_TEXT_TIMEOUT = 30
PLOT_TIMEOUT = 60
WEATHER_TIMEOUT = 30
# Лимит размера base64 для plot (байты после декодирования), 10 MB
PLOT_MAX_IMAGE_BYTES = 10 * 1024 * 1024

# Сообщение в stderr/error при отсутствии данных (404)
STDERR_404_MARKER = "Данных нет"

# Сообщения пользователю
MSG_MODULE_NOT_FOUND = f'Модуль "{MODULE_NAME}" не найден'
MSG_404 = "Не найдены данные по операции"
MSG_ERROR_PREFIX = "Произошла ошибка обработки: "
MSG_USER_UNKNOWN_ERROR = "Ошибка выполнения операции"


# ----------------------------------------------------------
def _run_solar_cli(
    operation: str,
    date_str: str | None = None,
    start_str: str | None = None,
    end_str: str | None = None,
    city_str: str | None = None,
    content_type: str = "plain",
    service: str = "weatherapi",
    extended: bool = False,
    timeout_sec: int = 30,
) -> tuple[int, bytes, bytes]:
    """
    Запускает cli.py с заданной операцией. Мультиплатформенный вызов (Windows: CREATE_NO_WINDOW).

    Returns:
        (returncode, stdout_bytes, stderr_bytes)

    Raises:
        FileNotFoundError: CLI или интерпретатор не найден.
        subprocess.TimeoutExpired: таймаут выполнения.
    """
    if not os.path.isfile(MODULE_CLI):
        raise FileNotFoundError(f'Не найден модуль "{MODULE_NAME}"')

    if operation == "plot":
        if not start_str or not end_str:
            raise ValueError("plot requires start_str and end_str")
        argv = [
            sys.executable,
            MODULE_CLI,
            "plot",
            "--start",
            start_str.strip(),
            "--end",
            end_str.strip(),
            "--format",
            "json",
        ]
    elif operation == "weather":
        if not city_str or not city_str.strip():
            raise ValueError("weather requires city_str")
        argv = [
            sys.executable,
            MODULE_CLI,
            "weather",
            "--city",
            city_str.strip(),
            "--format",
            "json",
            "--content-type",
            content_type
        ]
        if extended:
            argv.append("--extended")
    else:
        if not date_str or not date_str.strip():
            raise ValueError(f"{operation} requires date_str")
        argv = [
            sys.executable,
            MODULE_CLI,
            operation,
            "--date",
            date_str.strip(),
            "--format",
            "json",
        ]

    run_kwargs: dict = {
        "cwd": MODULE_DIR,
        "capture_output": True,
        "timeout": timeout_sec,
        "shell": False,
    }
    if sys.platform == "win32":
        run_kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

    proc = subprocess.run(argv, **run_kwargs)
    stdout_bytes = proc.stdout or b""
    stderr_bytes = proc.stderr or b""
    return (proc.returncode, stdout_bytes, stderr_bytes)


# Лимит длины stdout в логе при ошибке парсинга (символы)
_PARSE_ERROR_STDOUT_LOG_LIMIT = 3000


# ----------------------------------------------------------
def _parse_json_text_response(
    returncode: int,
    stdout_bytes: bytes,
    stderr_bytes: bytes,
    logger_var=None,
) -> tuple[bool, str, str | None]:
    """
    Парсит ответ CLI для solar-noon и solar-times-text (JSON с data.result).

    Returns:
        (success, value, error_kind). value = текст при успехе; при ошибке — детали для лога.
        error_kind in (None, "module_not_found", "404", "other").
    """
    stderr_str = stderr_bytes.decode("utf-8", errors="replace").strip()
    stdout_str = stdout_bytes.decode("utf-8", errors="replace").strip()

    if returncode != 0:
        if STDERR_404_MARKER in stderr_str:
            return (False, stderr_str, "404")
        return (False, stderr_str or f"Код возврата {returncode}", "other")

    try:
        obj = json.loads(stdout_str)
    except (json.JSONDecodeError, TypeError) as e:
        if logger_var is not None:
            logger_var.error("Ошибка парсинга JSON: %s", e)
            log_stdout = (
                stdout_str
                if len(stdout_str) <= _PARSE_ERROR_STDOUT_LOG_LIMIT
                else stdout_str[:_PARSE_ERROR_STDOUT_LOG_LIMIT] + "..."
            )
            logger_var.error("Ответ CLI (stdout): %s", log_stdout)
        return (False, f"Ошибка парсинга JSON: {e}", "other")

    if not obj.get("success"):
        err = obj.get("error") or {}
        msg = err.get("message", "Неизвестная ошибка")
        code = err.get("code")
        if code == 404 or STDERR_404_MARKER in str(msg):
            return (False, msg, "404")
        return (False, msg, "other")

    result = (obj.get("data") or {}).get("result")
    if result is None:
        return (False, "В ответе нет data.result", "other")
    return (True, str(result), None)


def _parse_plot_response(
    returncode: int,
    stdout_bytes: bytes,
    stderr_bytes: bytes,
    start_str: str,
    end_str: str,
    max_base64_decoded_bytes: int = PLOT_MAX_IMAGE_BYTES,
) -> tuple[bool, tuple[str, str, str] | None, str | None]:
    """
    Парсит ответ CLI для plot (JSON с data.image_base64).

    Returns:
        (success, value, error_kind). value = (base64_str, start_str, end_str) при успехе; иначе None.
        error_kind in (None, "404", "other").
    """
    stderr_str = stderr_bytes.decode("utf-8", errors="replace").strip()
    stdout_str = stdout_bytes.decode("utf-8", errors="replace").strip()

    if returncode != 0:
        if STDERR_404_MARKER in stderr_str:
            return (False, None, "404")
        return (False, None, "other")

    try:
        obj = json.loads(stdout_str)
    except (json.JSONDecodeError, TypeError):
        return (False, None, "other")

    if not obj.get("success"):
        err = obj.get("error") or {}
        code = err.get("code")
        if code == 404:
            return (False, None, "404")
        return (False, None, "other")

    data = obj.get("data") or {}
    b64 = data.get("image_base64")
    if not b64 or not isinstance(b64, str):
        return (False, None, "other")

    # Проверка размера: base64 декодируется в ~3/4 от длины строки
    if len(b64) > (max_base64_decoded_bytes * 4 // 3):
        return (False, None, "other")

    try:
        decoded = base64.b64decode(b64, validate=True)
    except Exception:
        return (False, None, "other")
    if len(decoded) > max_base64_decoded_bytes:
        return (False, None, "other")

    return (True, (b64, start_str, end_str), None)


def _to_user_message(
    success: bool,
    value: str | tuple[str, str, str] | None,
    error_kind: str | None,
    prefix_success: str | None = None,
) -> str:
    """
    Формирует строку для отправки пользователю (текстовые ответы).

    prefix_success: при успехе — префикс перед value (например "Сегодня полдень в ").
    """
    if success and value is not None:
        if isinstance(value, tuple):
            text = str(value[0])  # для единообразия не используется в текстовом ответе
        else:
            text = str(value)
        if prefix_success is not None:
            return prefix_success + text
        return text
    if error_kind == "module_not_found":
        return MSG_MODULE_NOT_FOUND
    if error_kind == "404":
        return MSG_404
    # Неизвестная ошибка
    # Не показываем пользоватеою ненужные подробности
    #    detail = value if isinstance(value, str) else "Неизвестная ошибка"
    #    return MSG_ERROR_PREFIX + '3' + detail
    return MSG_USER_UNKNOWN_ERROR


# ----------------------------------------------------------
# Публичный API для бота
# ----------------------------------------------------------


# ----------------------------------------------------------
def get_solar_noon(logger_var):
    """Запрашивает время полдня на сегодня. Возвращает строку для чата."""
    today = datetime.date.today().strftime("%d.%m.%Y")
    # today = datetime.date(1980, 1, 1).strftime("%d.%m.%Y") # Для отладки. Несуществующая дата
    try:
        returncode, stdout_bytes, stderr_bytes = _run_solar_cli(
            "solar-noon", date_str=today, timeout_sec=SOLAR_NOON_TIMEOUT
        )
    except FileNotFoundError:
        return _to_user_message(False, None, "module_not_found", prefix_success="")
    except subprocess.TimeoutExpired:
        logger_var.error(
            "solar_noon timeout at %s", datetime.datetime.now()
        )
        return _to_user_message(
            False, "Таймаут выполнения", "other", prefix_success=""
        )

    success, value, error_kind = _parse_json_text_response(
        returncode, stdout_bytes, stderr_bytes, logger_var=logger_var
    )
    if success:
        return _to_user_message(True, value, None, prefix_success="Сегодня полдень в ")
    if error_kind == "404":
        return "Нет данных на сегодня"
    if error_kind == "other":
        logger_var.error("solar_noon error: %s at %s", value, datetime.datetime.now())
    return _to_user_message(False, value, error_kind, prefix_success="")


# ----------------------------------------------------------
def get_solar_times_text(logger_var):
    """Запрашивает текст солнечных времён на сегодня. Возвращает строку для чата."""
    today = datetime.date.today().strftime("%d.%m.%Y")
    # today = datetime.date(1980, 1, 1).strftime("%d.%m.%Y") # Для отладки. Несуществующая дата
    try:
        returncode, stdout_bytes, stderr_bytes = _run_solar_cli(
            "solar-times-text", date_str=today, timeout_sec=SOLAR_TIMES_TEXT_TIMEOUT
        )
    except FileNotFoundError:
        return _to_user_message(False, None, "module_not_found", prefix_success="")
    except subprocess.TimeoutExpired:
        logger_var.error(
            "solar_times_text timeout at %s", datetime.datetime.now()
        )
        return _to_user_message(
            False, "Таймаут выполнения", "other", prefix_success=""
        )

    success, value, error_kind = _parse_json_text_response(
        returncode, stdout_bytes, stderr_bytes, logger_var=logger_var
    )
    if success:
        return _to_user_message(True, value, None, prefix_success=None)
    if error_kind == "404":
        return "Нет данных на сегодня"
    if error_kind == "other":
        logger_var.error(
            "solar_times_text error: %s at %s", value, datetime.datetime.now()
        )
    return _to_user_message(False, value, error_kind, prefix_success="")


# ----------------------------------------------------------
def get_weather_text(
    logger_var,
    city: str = "spb",
    content_type: str = "html",
    service: str = "weatherapi",
    extended: bool = False,
):
    """Запрашивает погоду по коду города через CLI weather. Возвращает строку для чата (HTML или plain)."""
    try:
        returncode, stdout_bytes, stderr_bytes = _run_solar_cli(
            "weather",
            city_str=city,
            content_type=content_type,
            service=service,
            extended=extended,
            timeout_sec=WEATHER_TIMEOUT,
        )
    except FileNotFoundError:
        return _to_user_message(False, None, "module_not_found", prefix_success="")
    except subprocess.TimeoutExpired:
        logger_var.error(
            "get_weather_text timeout at %s", datetime.datetime.now()
        )
        return _to_user_message(
            False, "Таймаут выполнения", "other", prefix_success=""
        )

    success, value, error_kind = _parse_json_text_response(
        returncode, stdout_bytes, stderr_bytes, logger_var=logger_var
    )
    if success:
        return _to_user_message(True, value, None, prefix_success=None)
    if error_kind == "404":
        return "Нет данных по погоде"
    if error_kind == "other":
        logger_var.error(
            "get_weather_text error: %s at %s", value, datetime.datetime.now()
        )
    return _to_user_message(False, value, error_kind, prefix_success="")


def _plural_form(
    n: int,
    word_one: str = "день",
    word_few: str = "дня",
    word_many: str = "дней",
) -> str:
    """Возвращает одну из трёх форм по числу n: 1/21/31… — word_one, 2–4/22–24… — word_few, иначе word_many. По умолчанию «день»/«дня»/«дней»."""
    if n % 10 == 1 and n % 100 != 11:
        return word_one
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return word_few
    return word_many


# ----------------------------------------------------------
def get_solar_plot(logger_var) -> tuple[bytes | None, str]:
    """
    Запрашивает график солнечной активности за период (сегодня −30 … сегодня +30 дней).

    Returns:
        (image_bytes, caption_or_error_message):
        - При успехе: (bytes, "График солнечной активности за 60 дней").
        - При ошибке: (None, строка сообщения об ошибке для пользователя).
    """
    PLOT_DAYS = 60  # полная длина периода графика (середина — сегодня)
    today = datetime.date.today()
    half = PLOT_DAYS // 2
    start_date = today - datetime.timedelta(days=half)
    end_date = today + datetime.timedelta(days=half)
    start_str = start_date.strftime("%d.%m.%Y")
    end_str = end_date.strftime("%d.%m.%Y")
    caption_ok = f"График солнечной активности за {PLOT_DAYS} {_plural_form(PLOT_DAYS, 'день', 'дня', 'дней')}"

    try:
        returncode, stdout_bytes, stderr_bytes = _run_solar_cli(
            "plot",
            start_str=start_str,
            end_str=end_str,
            timeout_sec=PLOT_TIMEOUT,
        )
    except FileNotFoundError:
        return (None, MSG_MODULE_NOT_FOUND)
    except subprocess.TimeoutExpired:
        logger_var.error(
            "solar_plot timeout at %s", datetime.datetime.now()
        )
        return (None, MSG_ERROR_PREFIX + "Таймаут выполнения")

    success, value, error_kind = _parse_plot_response(
        returncode, stdout_bytes, stderr_bytes, start_str, end_str
    )
    if success and value is not None:
        b64_str, _, _ = value
        try:
            image_bytes = base64.b64decode(b64_str, validate=True)
            return (image_bytes, caption_ok)
        except Exception as e:
            logger_var.error(
                "solar_plot decode error: %s at %s", e, datetime.datetime.now()
            )
            return (None, MSG_ERROR_PREFIX + "Ошибка декодирования графика")

    if error_kind == "other":
        stderr_str = (stderr_bytes or b"").decode("utf-8", errors="replace").strip()
        logger_var.error(
            "solar_plot error: %s at %s", stderr_str or "unknown", datetime.datetime.now()
        )
    return (None, _to_user_message(False, None, error_kind, prefix_success=""))

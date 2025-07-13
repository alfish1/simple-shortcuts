from os import getenv
from datetime import datetime, timedelta, UTC

from .default import DEFAULT


class Config:
    """
    Globally adjustable module defaults.

    Make sure to adjust the values BEFORE calling any functions from the module.

    Some values can also be adjusted by setting the appropriate environment variable.

    Example:
        from shortcuts.date import Config, time_now

        Config.naive = False

        print(time_now())  # 2025-07-13 15:44:53.711417-04:00
    """

    # use naive datetime objects. defaults to true
    naive: bool = getenv('SHORTCUTS_DATE_NAIVE', 'true').lower() == 'true'

    # use utc time instead of local time. defaults to false
    utc: bool = getenv('SHORTCUTS_DATE_UTC', 'false').lower() == 'true'

    # default timestamp format string
    format: str = '%Y-%m-%dT%H:%M:%S.%f'


def _time_value(naive, utc, add=False, subtract=False, **intervals):
    """
    Internal utility function that returns requested datetime object, optionally adding/subtracting interval values
    """

    # set defaults
    if naive is DEFAULT:
        naive = Config.naive

    if utc is DEFAULT:
        utc = Config.utc

    # generate requested datetime value
    if utc:
        value = datetime.now(UTC)

        if naive:
            value = value.replace(tzinfo=None)

    else:
        value = datetime.now()

        if not naive:
            value = value.astimezone()

    # add/subtract intervals
    if add:
        value = value + timedelta(**intervals)

    elif subtract:
        value = value - timedelta(**intervals)

    return value


def time_now(
        *,
        naive: bool = DEFAULT,
        utc: bool = DEFAULT
) -> datetime:
    """
    Get current datetime.

    Set naive=False to get a timezone-aware value.

    Set utc=True to get utc time instead of local time.

    Use global `Config` object to adjust defaults.

    Args:
        naive: return timezone-naive datetime value. Defaults to true
        utc: return utc time instead of local time. Defaults to false

    Returns:
        datetime object
    """
    return _time_value(naive=naive, utc=utc)


def time_in(
        *,
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        days: int = 0,
        weeks: int = 0,
        microseconds: int = 0,
        milliseconds: int = 0,
        naive: bool = DEFAULT,
        utc: bool = DEFAULT
) -> datetime:
    """
    Get a future datetime value.

    Set naive=False to get a timezone-aware value.

    Set utc=True to get utc time instead of local time.

    Use global `Config` object to adjust defaults.

    Example:
        expire = time_in(seconds=5)

        expire = time_in(minutes=3, naive=False)  # timezone aware

        expire = time_in(hours=1, utc=True)  # utc time

    Args:
        seconds: number of seconds to add
        minutes: number of minutes to add
        hours: number of hours to add
        days: number of days to add
        weeks: number of weeks to add
        microseconds: number of microseconds to add
        milliseconds: number of milliseconds to add
        naive: return timezone-naive datetime value. Defaults to true
        utc: return utc time instead of local time. Defaults to false

    Returns:
        datetime object
    """

    return _time_value(
        naive=naive,
        utc=utc,
        add=True,
        seconds=seconds,
        minutes=minutes,
        hours=hours,
        days=days,
        weeks=weeks,
        microseconds=microseconds,
        milliseconds=milliseconds
    )


def time_ago(
        *,
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        days: int = 0,
        weeks: int = 0,
        microseconds: int = 0,
        milliseconds: int = 0,
        naive: bool = DEFAULT,
        utc: bool = DEFAULT
) -> datetime:
    """
    Get a past datetime value.

    Set naive=False to get a timezone-aware value.

    Set utc=True to get utc time instead of local time.

    Use global `Config` object to adjust defaults.

    Example:
        since = time_ago(seconds=5)

        since = time_ago(minutes=3, naive=False)  # timezone aware

        since = time_ago(hours=1, utc=True)  # utc time

    Args:
        seconds: number of seconds to subtract
        minutes: number of minutes to subtract
        hours: number of hours to subtract
        days: number of days to subtract
        weeks: number of weeks to subtract
        microseconds: number of microseconds to subtract
        milliseconds: number of milliseconds to subtract
        naive: return timezone-naive datetime value. Defaults to true
        utc: return utc time instead of local time. Defaults to false

    Returns:
        datetime object
    """

    return _time_value(
        naive=naive,
        utc=utc,
        subtract=True,
        seconds=seconds,
        minutes=minutes,
        hours=hours,
        days=days,
        weeks=weeks,
        microseconds=microseconds,
        milliseconds=milliseconds
    )


def timestamp(
        format: str = DEFAULT,
        *,
        utc: bool = DEFAULT
) -> str:
    """
    Get current datetime as a string.

    Use `format` param to specify custom `strftime` format.

    Set utc=True to get utc time instead of local time.

    Use global `Config` object to adjust defaults.

    Example:
        print(timestamp())  # 2025-06-22T16:54:58.507887

        print(timestamp('%Y-%m-%d %H:%M:%S'))  # 2025-06-22 16:54:58

    Args:
        format: `strftime` format string. defaults to `%Y-%m-%dT%H:%M:%S.%f`
        utc: use utc time instead of local time. Defaults to false

    Returns:
        datetime string
    """

    # get current datetime (tz-aware to support %z in format strings)
    now = _time_value(naive=False, utc=utc)

    # use default format
    if format is DEFAULT:
        format = Config.format

    # return formatted timestamp
    return now.strftime(format)

from os import getenv
from datetime import datetime, timedelta, UTC

from .default import DEFAULT


class Config:
    """
    Globally adjustable module defaults. Values can be adjusted by setting the appropriate environment variable, OR
    by overriding the Config class value BEFORE calling any functions from the module.

    Ie:
        from shortcuts.date import Config

        Config.naive = False
    """

    # return naive datetime object
    naive: bool = getenv('SHORTCUTS_DATE_NAIVE', 'true').lower() == 'true'

    # return utc time instead of local time
    utc: bool = getenv('SHORTCUTS_DATE_UTC', 'false').lower() == 'true'

    # default timestamp format string
    format: str = None


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

    Args:
        naive: Whether to return naive or timezone-aware datetime. Defaults to Config.naive value
        utc: Whether to return local or utc datetime. Defaults to Config.utc value

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
    Get a datetime value in the future. User can specify naive or timezone-aware, and local time or utc time.

    Example:
        expire = time_in(seconds=5)

        expire = time_in(minutes=3, naive=False)  # timezone aware

        expire = time_in(hours=1, utc=True)  # utc time

    Args:
        seconds: Number of seconds to add
        minutes: Number of minutes to add
        hours: Number of hours to add
        days: Number of days to add
        weeks: Number of weeks to add
        microseconds: Number of microseconds to add
        milliseconds: Number of milliseconds to add
        naive: Whether to return naive or timezone-aware datetime. Defaults to Config.naive value
        utc: Whether to return local or utc datetime. Defaults to Config.utc value

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
    Get a datetime value in the past. User can specify naive or timezone-aware, and local time or utc time.

    Example:
        since = time_ago(seconds=5)

        since = time_ago(minutes=3, naive=False)  # timezone aware

        since = time_ago(hours=1, utc=True)  # utc time

    Args:
        seconds: Number of seconds to subtract
        minutes: Number of minutes to subtract
        hours: Number of hours to subtract
        days: Number of days to subtract
        weeks: Number of weeks to subtract
        microseconds: Number of microseconds to subtract
        milliseconds: Number of milliseconds to subtract
        naive: Whether to return naive or timezone-aware datetime. Defaults to Config.naive value
        utc: Whether to return local or utc datetime. Defaults to Config.utc value

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
        format: str = None,
        *,
        utc: bool = DEFAULT
) -> str:
    """
    Get current datetime string.

    User can specify local time or utc time.

    User can also specify exact python `strftime` format string. Use Config.format to set global default value.

    Example:
        print(timestamp())  # '2025-06-22T16:54:58.507887'

        print(timestamp('%Y-%m-%d %H:%M:%S'))  # '2025-06-22 16:54:58'

        print(timestamp(utc=True))  # '2025-06-22T20:54:58.507887'

    Args:
        format: `strftime` format string
        utc: Whether to return local or utc timestamp. Defaults to Config.utc value

    Returns:
        datetime string
    """

    # get current datetime
    now = _time_value(naive=False, utc=utc)

    # user specified format
    if format:
        pass

    # user specified global format
    elif Config.format:
        format = Config.format

    # use default naive format
    elif Config.naive:
        format = '%Y-%m-%dT%H:%M:%S.%f'

    # use default timezone-aware format
    else:
        format = '%Y-%m-%dT%H:%M:%S.%f%z'

    # return formatted timestamp
    return now.strftime(format)


# moving duration and difference to backup branch
class Duration:
    """
    Simple duration class for easily retrieving TOTAL interval values, ie: total seconds, total minutes etc, rounded
    down to strip decimal places, so that user gets the SECONDS ONLY etc.

    Supports all standard timedelta values: seconds, minutes, hours, days, weeks, microseconds, milliseconds.

    Sample usage:
        # get timedelta interval between two datetime variables
        interval = finished_date - started_date

        # init duration class
        duration = Duration(interval)

        print(duration.seconds)  # prints total seconds (without decimals)
        print(duration.minutes)  # prints total minutes (without decimals)
    """

    # conversion constants
    class _convert:
        minutes = 60
        hours = 3600
        days = 86400
        weeks = 604800
        microseconds = 1_000_000
        milliseconds = 1000

    def __init__(self, interval: timedelta):
        self._interval = interval

        self._total_seconds = interval.total_seconds()

        # cache computed values to avoid recomputing
        self._cache = {}

    def _compute(self, unit, divide=None, multiply=None):
        # return cached computed value
        if unit in self._cache:
            return self._cache[unit]

        # compute unit value using timedelta's total_seconds value
        value = self._total_seconds

        if divide:
            value /= divide

        elif multiply:
            value *= multiply

        # remove decimal places
        value = int(value)

        self._cache[unit] = value

        return value

    @property
    def seconds(self) -> int:
        """Return total seconds."""
        return self._compute('seconds')

    @property
    def minutes(self) -> int:
        """Return total minutes."""
        return self._compute('minutes', divide=self._convert.minutes)

    @property
    def hours(self) -> int:
        """Return total hours."""
        return self._compute('hours', divide=self._convert.hours)

    @property
    def days(self) -> int:
        """Return total days."""
        return self._compute('days', divide=self._convert.days)

    @property
    def weeks(self) -> int:
        """Return total weeks."""
        return self._compute('weeks', divide=self._convert.weeks)

    @property
    def microseconds(self) -> int:
        """Return total microseconds."""
        return self._compute('microseconds', multiply=self._convert.microseconds)

    @property
    def milliseconds(self) -> int:
        """Return total milliseconds."""
        return self._compute('milliseconds', multiply=self._convert.milliseconds)

    def __repr__(self):
        return str(self._interval)


def difference(value1: datetime, value2: datetime) -> Duration:
    """
    Compare two datetimes to each other and return a Duration instance, never returning a negative interval.

    Example:
        diff = difference(create_date, complete_date)

        print(f"{diff.hours}:{diff.minutes}:{diff.seconds}.{diff.milliseconds}")

    Args:
        value1: datetime value one
        value2: datetime value two

    Returns:
        Duration object
    """
    # get positive interval difference
    interval = abs(value1 - value2)

    # return duration instance
    return Duration(interval)

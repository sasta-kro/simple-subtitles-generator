import datetime

def format_timestamp(seconds: float) -> str:
    """
    # format_timestamp formats a float of seconds into a SRT timestamp string.

    Args:
        seconds: The time in seconds.

    Returns:
        A string in the format 'HH:MM:SS,mmm'.
    """
    delta = datetime.timedelta(seconds=seconds)
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = delta.microseconds // 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

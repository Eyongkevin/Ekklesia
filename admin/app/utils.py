from datetime import datetime

def get_short_desc(desc: str, max_length: int = 50) -> str | None:
    return desc[:max_length] + '...'

def format_datetime(dt: datetime) -> str:
    if dt is None:
        return "N/A"
    return dt.strftime("%A, %d %B %Y at %I:%M %p")
def get_short_desc(desc: str, max_length: int = 50) -> str | None:
    return desc[:max_length] + '...'

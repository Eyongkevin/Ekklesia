def get_short_desc(desc: str) -> str | None:
    if desc:
        return desc[:50] + '...'
    return desc
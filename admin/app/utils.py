from datetime import datetime

class Colors:
    PURPLE = "#6c5ce7"
    PURPLE_LIGHT = "#ece9ff"
    PURPLE_MID = "#a89df5"
    BG = "#f4f4f8"
    WHITE = "#ffffff"
    BORDER = "1px solid #e8e8ec"
    MUTED = "#888888"
    DARK = "#1a1b3a"
    GREEN = "#10b981"

btn_primary_style = dict(
    background=Colors.GREEN,
    color=Colors.WHITE,
    border_radius="10px",
    padding="0.8em 1.2em",
    font_size="13px",
    font_weight="600",
    cursor="pointer",
    display="flex",
    align_items="center",
    gap="0.5em",
    border="none",
    align="center",
    _hover={"background": "#0b9e6d"},
)

btn_ghost_style = dict(
    background=Colors.WHITE,
    border=Colors.BORDER,
    color="#444",
    border_radius="8px",
    padding="9px 18px",
    font_size="13px",
    font_weight="500",
    cursor="pointer",
    _hover={"background": "#f5f5f8"},
)

def get_short_desc(desc: str, max_length: int = 50) -> str | None:
    return desc[:max_length] + '...'

def format_datetime(dt: datetime) -> str:
    if dt is None:
        return "N/A"
    return dt.strftime("%A, %d %B %Y at %I:%M %p")
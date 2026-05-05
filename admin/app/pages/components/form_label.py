import reflex as rx

def form_label(label: str, text_color: str="", size: str = '1', font_weight: str="bold", required: bool=False):
    return rx.hstack(
            rx.text(label, font_weight=font_weight, size=size, color=text_color),
            rx.cond(
                required,
                rx.text(
                    "*",
                    color="red",
                    font_size="0.7em",
                    vertical_align="super",
                ),
            ),
            spacing="1",
    )

import reflex as rx

def pagination_controls(state):
    return rx.hstack(
        rx.button(
            "Previous",
            on_click=state.prev_page,
            disabled=state.page == 1,
        ),

        rx.text(
            f"Page {state.page} of {state.total_pages}"
        ),

        rx.button(
            "Next",
            on_click=state.next_page,
            disabled=state.page == state.total_pages,
        ),

        justify="end",
        width="100%",
        padding_top="1em",
    )
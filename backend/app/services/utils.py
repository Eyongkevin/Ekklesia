def resolve_filter(item: str) -> bool | int | str | None:
        if item == "All":
            return
        if item == "True":
            return True
        elif item == "False":
            return False
        try:
            return int(item)
        except ValueError:
            pass
        return item
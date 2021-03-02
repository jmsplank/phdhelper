class Error(Exception):
    def __init__(self, additional):
        self.message = (
            "\nThis error is defined by phdhelper\n----------------------------------\n"
        )
        self.message += additional
        super().__init__(self.message)


class OutOfBoundsException(Error):
    def __init__(self, value, limit, small=False, additional=None):
        self.message = f"Value out of bounds (too {'big' if not small else 'small'})."
        self.message += f"\n{value} {'>' if not small else '<'} {limit}"
        self.message += f"\n{additional}"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"

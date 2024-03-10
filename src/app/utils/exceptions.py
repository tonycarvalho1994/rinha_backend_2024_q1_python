class InvalidDescriptionError(Exception):
    def __init__(self, descr: str):
        self.message = f"Invalid description: {descr}."
        super().__init__(self.message)


class CustomerNotFoundError(Exception):
    ...


class LimitExceededError(Exception):
    ...

class Error:
    """
    Custom error class to handle exceptions.
    """

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"Error: {self.message}"

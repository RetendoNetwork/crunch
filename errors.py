class Error(Exception):
    def __init__(self, scope, error):
        self.scope = scope
        self.error = error

    def __str__(self):
        return f"crunch: {self.scope}: {self.error}"

BufferOverreadError = Error(
    scope="buffer",
    error="read exceeds buffer capacity"
)

BufferUnderreadError = Error(
    scope="buffer",
    error="read offset is less than zero"
)

BufferOverwriteError = Error(
    scope="buffer",
    error="write offset exceeds buffer capacity"
)

BufferUnderwriteError = Error(
    scope="buffer",
    error="write offset is less than zero"
)

BufferInvalidByteCountError = Error(
    scope="buffer",
    error="invalid byte count requested"
)

BytesBufNegativeReadError = Error(
    scope="bytesbuf",
    error="reader returned negative count from Read"
)

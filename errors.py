class Error(Exception):
    """
    Error implements a custom error type used in crunch.
    """
    def __init__(self, scope, error):
        self.scope = scope
        self.error = error

    def __str__(self):
        return f"crunch: {self.scope}: {self.error}"

BufferOverreadError = Error("buffer", "read exceeds buffer capacity")

BufferUnderreadError = Error("buffer", "read offset is less than zero")

BufferOverwriteError = Error("buffer", "write offset exceeds buffer capacity")

BufferUnderwriteError = Error("buffer", "write offset is less than zero")

BufferInvalidByteCountError = Error("buffer", "invalid byte count requested")

BytesBufNegativeReadError = Error("bytesbuf", "reader returned negative count from Read")
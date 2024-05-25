from typing import NamedTuple, Callable


class ResponseHandler(NamedTuple):
    """A pending response callback, waiting for a response to one of our messages"""

    # requestId: int - used only as a key
    callback: Callable
    # FIXME, add timestamp and age out old requests

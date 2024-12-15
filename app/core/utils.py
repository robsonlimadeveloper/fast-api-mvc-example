from starlette.types import Send, Scope, Receive

class AsyncIterator:
    def __init__(self, body: bytes):
        self.body = body
        self.sent = False

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.sent:
            self.sent = True
            return self.body
        raise StopAsyncIteration
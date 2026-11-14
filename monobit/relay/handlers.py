from tornado.websocket import WebSocketHandler


class RelayHandler(WebSocketHandler):
    async def on_message(self, message):
        self.write_message(message)
class PingUseCase:

    def __init__(self):
        pass

    @staticmethod
    def do_ping(msg: str) -> str:
        return msg.lower().replace("ping", "pong")

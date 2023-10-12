import datetime


class HelloUseCase:

    def __init__(self):
        pass

    @staticmethod
    def get_saludo() -> str:
        hh = datetime.datetime.now()
        h = hh.hour
        if 6 <= h < 12:
            return "Hola Buenos días"
        if 12 <= h < 21:
            return "Hola Buenas tardes"
        if 21 <= h < 6:
            return "Hola Buenas noches"

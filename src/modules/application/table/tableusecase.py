from typing import List


class TableUseCase:

    def __init__(self):
        pass

    @staticmethod
    def get_table_headers() -> List:
        return ["Letra", "Número", "a"]

    @staticmethod
    def get_table_values() -> List:
        return [["a", 1, "analfabeto"], ["b", 2, "bicarbonato"]]

class MoveError(Exception):
    def __init__(self,  error_type: int, coordinates: list = None):
        self.__coordinates = coordinates
        self.__type = error_type

    def __str__(self):
        if self.__type == 0:
            return f"Nie można przemieścić jednostki. Na tych współrzędnych {self.__coordinates} jest inna jednostka!"
        elif self.__type == 1:
            return "Przekroczyłeś limit ruchu dla danej jednostki!"


class AttackError(Exception):
    def __init__(self, error_type: int):
        self.__type = error_type

    def __str__(self):
        if self.__type == 0:
            return "Nie można zaatakować tej jednostki. Ta jednostka jest po twojej stronie!"
        elif self.__type == 1:
            return "Nie można zaatakować tej jednostki. Cel poza zasięgiem!"

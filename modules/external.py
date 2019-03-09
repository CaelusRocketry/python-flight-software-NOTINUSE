class Sensor:
    def __init__(self, name: str, normal: float, warn: float, crit: float, get_data: function,  location: int) -> None:
        self.name = name
        self.normal = normal
        self.warn = warn
        self.crit = crit
        self.get_data = get_data
        self.location = location


def get_temp():
    # TODO: Actually write this
    pass


def get_pressure():
    pass


def get_attitude():
    pass


def get_flow_rate():
    pass

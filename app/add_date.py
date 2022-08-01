from datetime import datetime


def get_today():
    """
    Devuelve la fecha actual en el formato dd.mm.yyyy
    :return: La fecha actual en el formato de dd.mm.yyyy
    """
    return datetime.today().strftime("%d.%m.%Y")

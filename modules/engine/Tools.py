def convert_sec_to_min(sec_time):
    """
    Convertit un temps en secondes en (minutes, secondes).
    Ex : 125 -> (2, 5)
    """
    minutes = int(sec_time // 60)
    seconds = int(sec_time % 60)
    return (minutes, seconds)

def convert(time):
    pos = ["s","m","h","d"]
    time_dict = {"s": 1,"m": 60,"h": 3600,"d": 24*3600 }
    unit = time[-1]
    if unit not in pos:
        return -1
    try:
        timeVal = int(time[:-1])
    except:
        return -2

    return timeVal*time_dict[unit]
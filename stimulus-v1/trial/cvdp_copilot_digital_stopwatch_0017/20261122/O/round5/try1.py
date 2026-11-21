def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i < 3:
            reset = 1
            start_stop = 0
        elif i == 3:
            reset = 0
            start_stop = 0
        else:
            reset = 0
            if i < 6:
                start_stop = 0
            elif i < 10:
                start_stop = 1
            elif i < 14:
                start_stop = 0
            elif i < 22:
                start_stop = 1
            elif i < 26:
                start_stop = 0
            elif i < 40:
                start_stop = 1
            elif i < 44:
                start_stop = 0
            elif i < 60:
                start_stop = 1
            elif i < 64:
                start_stop = 0
            elif i < 100:
                start_stop = 1
            elif i < 104:
                start_stop = 0
            elif i < 200:
                start_stop = 1
            elif i < 204:
                start_stop = 0
            elif i < 400:
                start_stop = 1
            elif i < 404:
                start_stop = 0
            elif i < 800:
                start_stop = 1
            elif i < 804:
                start_stop = 0
            elif i < 1600:
                start_stop = 1
            elif i < 1604:
                start_stop = 0
            elif i < 2400:
                start_stop = 1
            elif i < 2404:
                start_stop = 0
            elif i < 3200:
                start_stop = 1
            elif i < 3204:
                start_stop = 0
            elif i < 3600:
                start_stop = 1
            elif i < 3604:
                start_stop = 0
            elif i < 3960:
                start_stop = 1
            else:
                start_stop = 0
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

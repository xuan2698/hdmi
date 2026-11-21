def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i == 0:
            reset = 1
            start_stop = 0
        elif i == 2:
            reset = 0
            start_stop = 0
        elif i == 4:
            start_stop = 1
        elif i == 60:
            start_stop = 0
        elif i == 70:
            start_stop = 1
        elif i == 200:
            reset = 1
        elif i == 202:
            reset = 0
            start_stop = 0
        elif i == 205:
            start_stop = 1
        elif i == 500:
            start_stop = 0
        elif i == 520:
            start_stop = 1
        elif i == 1000:
            reset = 1
        elif i == 1002:
            reset = 0
            start_stop = 1
        elif i == 1600:
            start_stop = 0
        elif i == 1650:
            start_stop = 1
        elif i == 2200:
            reset = 1
        elif i == 2202:
            reset = 0
            start_stop = 0
        elif i == 2205:
            start_stop = 1
        elif i == 2800:
            start_stop = 0
        elif i == 2850:
            start_stop = 1
        elif i == 3400:
            reset = 1
        elif i == 3402:
            reset = 0
            start_stop = 1
        elif i == 3900:
            start_stop = 0
        elif i == 3950:
            start_stop = 1
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

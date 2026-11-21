def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i == 0:
            reset = 1
            start_stop = 0
        elif i == 3:
            reset = 0
            start_stop = 0
        elif i == 5:
            start_stop = 1
        elif i == 500:
            start_stop = 0
        elif i == 600:
            start_stop = 1
        elif i == 1200:
            reset = 1
        elif i == 1203:
            reset = 0
            start_stop = 0
        elif i == 1205:
            start_stop = 1
        elif i == 1800:
            start_stop = 0
        elif i == 1900:
            start_stop = 1
        elif i == 2500:
            start_stop = 0
        elif i == 2600:
            start_stop = 1
        elif i == 3200:
            reset = 1
        elif i == 3203:
            reset = 0
            start_stop = 0
        elif i == 3205:
            start_stop = 1
        elif i == 3800:
            start_stop = 0
        elif i == 3900:
            start_stop = 1
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

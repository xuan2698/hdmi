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
        elif i == 6:
            start_stop = 0
        elif i == 8:
            start_stop = 1
        elif i == 100:
            start_stop = 0
        elif i == 200:
            start_stop = 1
        elif i == 500:
            reset = 1
        elif i == 502:
            reset = 0
            start_stop = 0
        elif i == 504:
            start_stop = 1
        elif i == 1000:
            start_stop = 0
        elif i == 1100:
            start_stop = 1
        elif i == 2000:
            reset = 1
        elif i == 2002:
            reset = 0
            start_stop = 1
        elif i == 3000:
            start_stop = 0
        elif i == 3100:
            start_stop = 1
        elif i == 3900:
            reset = 1
        elif i == 3902:
            reset = 0
            start_stop = 0
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

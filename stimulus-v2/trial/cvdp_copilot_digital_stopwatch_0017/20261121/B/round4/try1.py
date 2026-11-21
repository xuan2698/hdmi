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
            reset = 0
            start_stop = 1
        elif i == 120:
            start_stop = 0
        elif i == 180:
            start_stop = 1
        elif i == 400:
            reset = 1
        elif i == 402:
            reset = 0
            start_stop = 1
        elif i == 800:
            start_stop = 0
        elif i == 850:
            start_stop = 1
        elif i == 1200:
            reset = 1
        elif i == 1202:
            reset = 0
            start_stop = 0
        elif i == 1210:
            start_stop = 1
        elif i == 2000:
            start_stop = 0
        elif i == 2100:
            start_stop = 1
        elif i == 3000:
            reset = 1
        elif i == 3002:
            reset = 0
            start_stop = 1
        elif i == 3600:
            start_stop = 0
        elif i == 3700:
            start_stop = 1
        rows.append({'reset': reset & 1, 'start_stop': start_stop & 1})
    return rows

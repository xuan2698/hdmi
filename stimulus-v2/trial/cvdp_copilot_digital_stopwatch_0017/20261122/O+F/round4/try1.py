def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i == 2:
            reset = 0
        if i == 4:
            start_stop = 1
        if i == 200:
            start_stop = 0
        if i == 260:
            start_stop = 1
        if i == 700:
            reset = 1
        if i == 702:
            reset = 0
        if i == 800:
            start_stop = 0
        if i == 900:
            start_stop = 1
        if i == 1400:
            start_stop = 0
        if i == 1500:
            start_stop = 1
        if i == 2000:
            reset = 1
        if i == 2002:
            reset = 0
        if i == 2100:
            start_stop = 0
        if i == 2200:
            start_stop = 1
        if i == 2800:
            start_stop = 0
        if i == 2900:
            start_stop = 1
        if i == 3400:
            reset = 1
        if i == 3402:
            reset = 0
        if i == 3500:
            start_stop = 0
        if i == 3600:
            start_stop = 1
        rows.append({'reset': reset & 1, 'start_stop': start_stop & 1})
    return rows

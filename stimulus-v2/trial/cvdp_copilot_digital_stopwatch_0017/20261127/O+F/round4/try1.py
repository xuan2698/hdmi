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
        elif i == 100:
            start_stop = 0
        elif i == 150:
            start_stop = 1
        elif i == 300:
            reset = 1
        elif i == 302:
            reset = 0
            start_stop = 0
        elif i == 305:
            start_stop = 1
        elif i == 800:
            start_stop = 0
        elif i == 900:
            start_stop = 1
        elif i == 1500:
            reset = 1
        elif i == 1502:
            reset = 0
            start_stop = 1
        elif i == 2500:
            start_stop = 0
        elif i == 2600:
            start_stop = 1
        elif i == 3500:
            reset = 1
        elif i == 3502:
            reset = 0
            start_stop = 0
        elif i == 3505:
            start_stop = 1
        elif i == 3800:
            start_stop = 0
        elif i == 3850:
            start_stop = 1
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

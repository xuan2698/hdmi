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
        elif i == 40:
            start_stop = 0
        elif i == 60:
            start_stop = 1
        elif i == 120:
            reset = 1
        elif i == 122:
            reset = 0
            start_stop = 1
        elif i == 300:
            start_stop = 0
        elif i == 340:
            start_stop = 1
        elif i == 700:
            reset = 1
        elif i == 702:
            reset = 0
            start_stop = 0
        elif i == 710:
            start_stop = 1
        elif i == 1500:
            start_stop = 0
        elif i == 1560:
            start_stop = 1
        elif i == 2500:
            reset = 1
        elif i == 2502:
            reset = 0
            start_stop = 1
        elif i == 3500:
            start_stop = 0
        elif i == 3560:
            start_stop = 1
        elif i == 3900:
            reset = 1
        elif i == 3902:
            reset = 0
            start_stop = 1
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

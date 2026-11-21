def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i == 2:
            reset = 0
        if i == 4:
            start_stop = 1
        if i == 40:
            start_stop = 0
        if i == 60:
            start_stop = 1
        if i == 200:
            reset = 1
        if i == 203:
            reset = 0
        if i == 220:
            start_stop = 0
        if i == 240:
            start_stop = 1
        if i == 800:
            start_stop = 0
        if i == 820:
            start_stop = 1
        if i == 1500:
            reset = 1
        if i == 1503:
            reset = 0
        if i == 1520:
            start_stop = 0
        if i == 1540:
            start_stop = 1
        if i == 2500:
            start_stop = 0
        if i == 2520:
            start_stop = 1
        if i == 3500:
            reset = 1
        if i == 3503:
            reset = 0
        if i == 3520:
            start_stop = 0
        if i == 3540:
            start_stop = 1
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

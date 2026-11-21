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
        elif i < 40:
            reset = 0
            start_stop = 1
        else:
            if rng.random() < 0.015:
                reset = 1
            else:
                reset = 0
            if rng.random() < 0.04:
                start_stop = 1 - start_stop
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

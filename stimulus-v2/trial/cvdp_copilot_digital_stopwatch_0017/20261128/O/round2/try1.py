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
            if rng.random() < 0.02:
                reset = 1
            else:
                reset = 0
            if rng.random() < 0.05:
                start_stop = 1 - start_stop
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

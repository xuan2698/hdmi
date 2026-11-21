def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i < 3:
            reset = 1
            start_stop = 0
        elif i < 6:
            reset = 0
            start_stop = 0
        else:
            reset = 0
            phase = (i - 6) % 500
            if phase < 2:
                start_stop = 0
            elif phase < 300:
                start_stop = 1
            elif phase < 310:
                start_stop = 0
            elif phase < 480:
                start_stop = 1
            else:
                start_stop = 0
            if rng.random() < 0.006:
                reset = 1
            if rng.random() < 0.02:
                start_stop = 1 - start_stop
        row = {
            'reset': reset,
            'start_stop': start_stop,
        }
        if rng.random() < 0.05:
            row['mid'] = {
                'reset': 1 if rng.random() < 0.1 else 0,
                'start_stop': 1 if rng.random() < 0.5 else 0,
            }
        rows.append(row)
    return rows

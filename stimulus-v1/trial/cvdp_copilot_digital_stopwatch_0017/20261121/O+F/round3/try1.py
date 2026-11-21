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
            phase = i % 500
            if phase < 3:
                start_stop = 0
            elif phase < 250:
                start_stop = 1
            elif phase < 260:
                start_stop = 0
            elif phase < 490:
                start_stop = 1
            else:
                start_stop = 0
            if rng.random() < 0.005:
                reset = 1
        row = {
            'reset': reset,
            'start_stop': start_stop,
        }
        if rng.random() < 0.02:
            row['mid'] = {
                'reset': 1 if rng.random() < 0.15 else 0,
                'start_stop': 1 if rng.random() < 0.5 else 0,
            }
        rows.append(row)
    return rows

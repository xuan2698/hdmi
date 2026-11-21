def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i < 4:
            reset = 1
            start_stop = 0
        elif i < 8:
            reset = 0
            start_stop = 0
        else:
            reset = 0
            phase = (i - 8) % 800
            if phase < 2:
                start_stop = 0
            elif phase < 400:
                start_stop = 1
            elif phase < 410:
                start_stop = 0
            elif phase < 790:
                start_stop = 1
            else:
                start_stop = 0
            if rng.random() < 0.003:
                reset = 1
        row = {
            'reset': reset,
            'start_stop': start_stop,
        }
        if rng.random() < 0.015:
            row['mid'] = {
                'reset': 1 if rng.random() < 0.1 else 0,
                'start_stop': 1 if rng.random() < 0.5 else 0,
            }
        rows.append(row)
    return rows

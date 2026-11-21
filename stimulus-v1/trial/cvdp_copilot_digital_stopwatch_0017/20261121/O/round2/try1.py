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
            phase = (i - 8) % 400
            if phase < 5:
                start_stop = 0
            elif phase < 200:
                start_stop = 1
            elif phase < 210:
                start_stop = 0
            elif phase < 395:
                start_stop = 1
            else:
                start_stop = 0
            if rng.random() < 0.015:
                reset = 1
        row = {
            'reset': reset,
            'start_stop': start_stop,
        }
        if rng.random() < 0.04:
            row['mid'] = {
                'reset': 1 if rng.random() < 0.25 else 0,
                'start_stop': 1 if rng.random() < 0.5 else 0,
            }
        rows.append(row)
    return rows

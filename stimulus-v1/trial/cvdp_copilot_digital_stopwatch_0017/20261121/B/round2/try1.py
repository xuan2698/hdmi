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
            phase = i % 200
            if phase < 5:
                start_stop = 0
            elif phase < 150:
                start_stop = 1
            elif phase < 160:
                start_stop = 0
            else:
                start_stop = 1
            if rng.random() < 0.015:
                reset = 1
            if rng.random() < 0.03:
                start_stop = 1 - start_stop
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

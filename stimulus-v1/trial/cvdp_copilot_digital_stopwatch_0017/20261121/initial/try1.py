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
            if i < 20:
                start_stop = 1
            elif i < 30:
                start_stop = 0
            elif i < 60:
                start_stop = 1
            elif i < 70:
                start_stop = 0
            elif i < 120:
                start_stop = 1
            elif i < 130:
                start_stop = 0
            elif i < 200:
                start_stop = 1
            elif i < 210:
                start_stop = 0
            elif i < 400:
                start_stop = 1
            elif i < 410:
                start_stop = 0
            elif i < 800:
                start_stop = 1
            elif i < 810:
                start_stop = 0
            elif i < 1600:
                start_stop = 1
            elif i < 1610:
                start_stop = 0
            elif i < 3200:
                start_stop = 1
            elif i < 3210:
                start_stop = 0
            else:
                start_stop = 1
            if rng.random() < 0.02:
                reset = 1
            else:
                reset = 0
        row = {
            'reset': reset,
            'start_stop': start_stop,
        }
        if rng.random() < 0.05:
            row['mid'] = {
                'reset': 1 if rng.random() < 0.3 else 0,
                'start_stop': 1 if rng.random() < 0.5 else 0,
            }
        rows.append(row)
    return rows

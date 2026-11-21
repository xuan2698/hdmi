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
            if i == 5:
                start_stop = 1
            elif i == 200:
                start_stop = 0
            elif i == 260:
                start_stop = 1
            elif i == 500:
                start_stop = 0
            elif i == 520:
                start_stop = 1
            elif i == 1000:
                start_stop = 0
            elif i == 1010:
                start_stop = 1
            elif i == 5000:
                start_stop = 0
            elif i == 5010:
                start_stop = 1
            elif i == 15000:
                start_stop = 0
            elif i == 15010:
                start_stop = 1
            elif i == 19000:
                start_stop = 0
            elif i == 19010:
                start_stop = 1
            if rng.random() < 0.0005 and i > 100:
                reset = 1
            elif reset == 1 and rng.random() < 0.5:
                reset = 0
        rows.append({'reset': reset & 1, 'start_stop': start_stop & 1})
    return rows

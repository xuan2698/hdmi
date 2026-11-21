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
            if i == 4:
                start_stop = 1
            elif i == 200:
                start_stop = 0
            elif i == 260:
                start_stop = 1
            elif i == 1200:
                start_stop = 0
            elif i == 1250:
                start_stop = 1
            elif i == 2500:
                reset = 1
            elif i == 2503:
                reset = 0
                start_stop = 1
            elif i == 3600:
                start_stop = 0
            elif i == 3650:
                start_stop = 1
            elif rng.random() < 0.0008:
                start_stop ^= 1
            if i > 2503 and rng.random() < 0.00015:
                reset = 1
            elif reset == 1 and i > 2503 and rng.random() < 0.35:
                reset = 0
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

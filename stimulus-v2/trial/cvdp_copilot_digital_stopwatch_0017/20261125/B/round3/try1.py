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
            elif i == 5000:
                start_stop = 0
            elif i == 5100:
                start_stop = 1
            elif i == 15000:
                start_stop = 0
            elif i == 15050:
                start_stop = 1
            elif rng.random() < 0.0005:
                start_stop ^= 1
            if rng.random() < 0.0002:
                reset = 1
            elif reset == 1 and rng.random() < 0.3:
                reset = 0
        rows.append({'reset': reset & 1, 'start_stop': start_stop & 1})
    return rows

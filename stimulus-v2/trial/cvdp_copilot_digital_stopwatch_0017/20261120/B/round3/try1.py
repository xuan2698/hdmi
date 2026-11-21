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
            reset = 0
            phase = (i - 4) % 200
            if phase < 10:
                start_stop = 0
            elif phase < 100:
                start_stop = 1
            elif phase < 110:
                start_stop = 0
            else:
                start_stop = 1
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

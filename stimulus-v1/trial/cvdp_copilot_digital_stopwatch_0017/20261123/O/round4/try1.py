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
            if phase == 0:
                reset = 1
                start_stop = 0
            elif phase == 1:
                reset = 0
                start_stop = 0
            elif phase == 2:
                reset = 0
                start_stop = 1
            elif phase < 250:
                reset = 0
                start_stop = 1
            elif phase < 260:
                reset = 0
                start_stop = 0
            elif phase < 300:
                reset = 0
                start_stop = 1
            elif phase < 310:
                reset = 0
                start_stop = 0
            elif phase < 380:
                reset = 0
                start_stop = 1
            else:
                reset = 0
                start_stop = 0
        row = {'reset': reset, 'start_stop': start_stop}
        if i > 12 and i % 23 == 0:
            row['mid'] = {'start_stop': rng.randint(0, 1)}
        rows.append(row)
    return rows

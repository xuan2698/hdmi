def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i < 2:
            reset = 1
            start_stop = 0
        elif i == 2:
            reset = 0
            start_stop = 0
        else:
            reset = 0
            phase = (i - 3) % 40
            if phase < 2:
                start_stop = 0
            elif phase < 6:
                start_stop = 1
            elif phase < 8:
                start_stop = 0
            elif phase < 12:
                start_stop = 1
            elif phase < 14:
                start_stop = 0
            elif phase < 18:
                start_stop = 1
            elif phase < 20:
                start_stop = 0
            elif phase < 24:
                start_stop = 1
            elif phase < 26:
                start_stop = 0
            elif phase < 30:
                start_stop = 1
            elif phase < 32:
                start_stop = 0
            elif phase < 36:
                start_stop = 1
            else:
                start_stop = 0
        row = {'reset': reset, 'start_stop': start_stop}
        if i >= 3 and (i % 7 == 0):
            row['mid'] = {'start_stop': 1 - start_stop}
        rows.append(row)
    return rows

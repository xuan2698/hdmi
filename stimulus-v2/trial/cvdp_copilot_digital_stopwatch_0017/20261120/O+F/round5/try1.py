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
            phase = (i - 3) % 60
            if phase < 3:
                start_stop = 0
            elif phase < 8:
                start_stop = 1
            elif phase < 10:
                start_stop = 0
            elif phase < 15:
                start_stop = 1
            elif phase < 17:
                start_stop = 0
            elif phase < 22:
                start_stop = 1
            elif phase < 24:
                start_stop = 0
            elif phase < 29:
                start_stop = 1
            elif phase < 31:
                start_stop = 0
            elif phase < 36:
                start_stop = 1
            elif phase < 38:
                start_stop = 0
            elif phase < 43:
                start_stop = 1
            elif phase < 45:
                start_stop = 0
            elif phase < 50:
                start_stop = 1
            elif phase < 52:
                start_stop = 0
            elif phase < 57:
                start_stop = 1
            else:
                start_stop = 0
        row = {'reset': reset, 'start_stop': start_stop}
        if i >= 3 and (i % 11 == 0):
            row['mid'] = {'start_stop': 1 - start_stop}
        rows.append(row)
    return rows

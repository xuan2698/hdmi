def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i < 3:
            reset = 1
            start_stop = 0
        elif i < 5:
            reset = 0
            start_stop = 0
        else:
            reset = 0
            phase = (i - 5) % 500
            if phase < 3:
                start_stop = 0
            elif phase < 250:
                start_stop = 1
            elif phase < 253:
                start_stop = 0
            elif phase < 495:
                start_stop = 1
            else:
                start_stop = 0
        row = {'reset': reset, 'start_stop': start_stop}
        if i >= 5:
            phase = (i - 5) % 500
            if phase in (1, 251, 497):
                row['mid'] = {'start_stop': 1 - start_stop}
        rows.append(row)
    return rows

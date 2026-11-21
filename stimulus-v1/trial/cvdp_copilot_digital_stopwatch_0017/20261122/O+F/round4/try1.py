def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i < 4:
            reset = 1
            start_stop = 0
        elif i < 6:
            reset = 0
            start_stop = 0
        else:
            reset = 0
            phase = (i - 6) % 400
            if phase < 4:
                start_stop = 0
            elif phase < 200:
                start_stop = 1
            elif phase < 204:
                start_stop = 0
            elif phase < 396:
                start_stop = 1
            else:
                start_stop = 0
        row = {'reset': reset, 'start_stop': start_stop}
        if i >= 6 and (i - 6) % 400 in (2, 202, 398):
            row['mid'] = {'start_stop': 1 - start_stop}
        rows.append(row)
    return rows

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
            if i % 173 == 0:
                reset = 1
                start_stop = 0
            elif i % 173 == 1:
                reset = 0
                start_stop = 0
            elif i % 173 == 2:
                reset = 0
                start_stop = 1
            elif i % 89 == 0:
                start_stop = 1 - start_stop
            elif i % 47 == 0:
                start_stop = rng.randint(0, 1)
            elif i % 307 == 0:
                start_stop = 0
            elif i % 307 == 1:
                start_stop = 1
            elif i % 307 == 2:
                start_stop = 1
        row = {'reset': reset, 'start_stop': start_stop}
        if i > 12 and i % 11 == 0:
            row['mid'] = {'start_stop': rng.randint(0, 1)}
        elif i > 12 and i % 17 == 0:
            row['mid'] = {'start_stop': 0}
        elif i > 12 and i % 23 == 0:
            row['mid'] = {'start_stop': 1}
        rows.append(row)
    return rows

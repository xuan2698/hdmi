def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i < 3:
            reset = 1
            start_stop = 0
        elif i < 6:
            reset = 0
            start_stop = 0
        else:
            reset = 0
            if i % 97 == 0:
                start_stop = 1 - start_stop
            elif i % 53 == 0:
                start_stop = rng.randint(0, 1)
            elif i % 211 == 0:
                reset = 1
                start_stop = 0
            elif i % 211 == 1:
                reset = 0
                start_stop = 0
        row = {'reset': reset, 'start_stop': start_stop}
        if i % 7 == 0 and i > 10:
            row['mid'] = {'start_stop': rng.randint(0, 1)}
        rows.append(row)
    return rows

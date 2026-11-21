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
            if i % 211 == 0:
                reset = 1
                start_stop = 0
            elif i % 211 == 1:
                reset = 0
                start_stop = 0
            elif i % 211 == 2:
                reset = 0
                start_stop = 1
            elif i % 97 == 0:
                start_stop = 1 - start_stop
            elif i % 53 == 0:
                start_stop = rng.randint(0, 1)
            elif i % 401 == 0:
                start_stop = 0
            elif i % 401 == 1:
                start_stop = 1
            elif i % 401 == 2:
                start_stop = 1
            elif i % 401 == 3:
                start_stop = 0
        row = {'reset': reset, 'start_stop': start_stop}
        if i > 10 and i % 13 == 0:
            row['mid'] = {'start_stop': rng.randint(0, 1)}
        elif i > 10 and i % 19 == 0:
            row['mid'] = {'start_stop': 0}
        elif i > 10 and i % 29 == 0:
            row['mid'] = {'start_stop': 1}
        elif i > 10 and i % 37 == 0:
            row['mid'] = {'reset': 1, 'start_stop': 0}
        rows.append(row)
    return rows

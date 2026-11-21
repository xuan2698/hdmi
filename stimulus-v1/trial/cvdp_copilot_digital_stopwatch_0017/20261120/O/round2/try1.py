def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    mid = None
    for i in range(cycles):
        if i < 4:
            reset = 1
            start_stop = 0
        elif i == 4:
            reset = 0
            start_stop = 0
        elif i < 8:
            reset = 0
            start_stop = 0
        elif i < 40:
            reset = 0
            start_stop = 1
        elif i < 60:
            reset = 0
            start_stop = 0
        elif i < 200:
            reset = 0
            start_stop = 1
        else:
            r = rng.random()
            if r < 0.03:
                reset = 1
                start_stop = 0
            elif r < 0.06:
                reset = 0
                start_stop = 0
            elif r < 0.10:
                reset = 0
                start_stop = 1
            else:
                reset = 0
                if rng.random() < 0.5:
                    start_stop = 1
                else:
                    start_stop = 0
        row = {'reset': reset, 'start_stop': start_stop}
        if mid is not None:
            row['mid'] = mid
        rows.append(row)
        mid = None
        if i >= 4 and rng.random() < 0.03:
            mid = {'start_stop': 1 - start_stop}
    return rows

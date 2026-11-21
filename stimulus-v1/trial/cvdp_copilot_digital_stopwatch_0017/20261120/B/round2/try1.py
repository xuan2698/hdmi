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
        else:
            reset = 0
            if i < 12:
                start_stop = 0
            elif i < 40:
                start_stop = 1
            elif i < 60:
                start_stop = 0
            elif i < 120:
                start_stop = 1
            else:
                r = rng.random()
                if r < 0.04:
                    start_stop = 1 - start_stop
                elif r < 0.06:
                    reset = 1
                else:
                    reset = 0
        row = {'reset': reset, 'start_stop': start_stop}
        if mid is not None:
            row['mid'] = mid
        rows.append(row)
        mid = None
        if i >= 4 and rng.random() < 0.03:
            mid = {'start_stop': 1 - start_stop}
    return rows

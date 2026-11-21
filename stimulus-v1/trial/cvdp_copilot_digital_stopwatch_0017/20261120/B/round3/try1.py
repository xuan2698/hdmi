def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    mid = None
    for i in range(cycles):
        if i < 3:
            reset = 1
            start_stop = 0
        elif i == 3:
            reset = 0
            start_stop = 0
        else:
            reset = 0
            if i < 8:
                start_stop = 0
            elif i < 20:
                start_stop = 1
            elif i < 24:
                start_stop = 0
            elif i < 60:
                start_stop = 1
            elif i < 64:
                start_stop = 0
            elif i < 200:
                start_stop = 1
            else:
                r = rng.random()
                if r < 0.03:
                    start_stop = 1 - start_stop
                elif r < 0.045:
                    reset = 1
                else:
                    reset = 0
        row = {'reset': reset, 'start_stop': start_stop}
        if mid is not None:
            row['mid'] = mid
        rows.append(row)
        mid = None
        if i >= 3 and rng.random() < 0.02:
            mid = {'start_stop': 1 - start_stop}
    return rows

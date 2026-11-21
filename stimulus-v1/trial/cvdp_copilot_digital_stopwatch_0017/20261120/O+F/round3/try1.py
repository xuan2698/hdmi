def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    mid = None
    for i in range(cycles):
        if i < 3:
            reset = 1
            start_stop = 0
        elif i < 6:
            reset = 0
            start_stop = 0
        elif i < 10:
            reset = 0
            start_stop = 1
        elif i < 30:
            reset = 0
            start_stop = 1
        elif i < 34:
            reset = 0
            start_stop = 0
        elif i < 60:
            reset = 0
            start_stop = 1
        elif i < 64:
            reset = 0
            start_stop = 0
        elif i < 100:
            reset = 0
            start_stop = 1
        elif i < 104:
            reset = 0
            start_stop = 0
        elif i < 200:
            reset = 0
            start_stop = 1
        elif i < 204:
            reset = 0
            start_stop = 0
        elif i < 400:
            reset = 0
            start_stop = 1
        elif i < 404:
            reset = 0
            start_stop = 0
        elif i < 800:
            reset = 0
            start_stop = 1
        elif i < 804:
            reset = 0
            start_stop = 0
        elif i < 1600:
            reset = 0
            start_stop = 1
        elif i < 1604:
            reset = 0
            start_stop = 0
        elif i < 2400:
            reset = 0
            start_stop = 1
        elif i < 2404:
            reset = 0
            start_stop = 0
        elif i < 3200:
            reset = 0
            start_stop = 1
        elif i < 3204:
            reset = 0
            start_stop = 0
        elif i < 3600:
            reset = 0
            start_stop = 1
        elif i < 3604:
            reset = 0
            start_stop = 0
        else:
            reset = 0
            start_stop = 1
        row = {'reset': reset, 'start_stop': start_stop}
        if mid is not None:
            row['mid'] = mid
        rows.append(row)
        mid = None
        if i >= 6 and rng.random() < 0.02:
            mid = {'start_stop': 1 - start_stop}
        if i >= 6 and rng.random() < 0.005:
            mid = {'reset': 1}
    return rows

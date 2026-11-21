def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    mid = None
    for i in range(cycles):
        if i < 4:
            reset = 1
            start_stop = 0
        elif i < 8:
            reset = 0
            start_stop = 0
        elif i < 12:
            reset = 0
            start_stop = 1
        elif i < 20:
            reset = 0
            start_stop = 1
        elif i < 24:
            reset = 0
            start_stop = 0
        elif i < 60:
            reset = 0
            start_stop = 1
        elif i < 64:
            reset = 0
            start_stop = 0
        elif i < 200:
            reset = 0
            start_stop = 1
        elif i < 204:
            reset = 0
            start_stop = 0
        elif i < 600:
            reset = 0
            start_stop = 1
        elif i < 604:
            reset = 0
            start_stop = 0
        elif i < 1400:
            reset = 0
            start_stop = 1
        elif i < 1404:
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
        if i >= 8 and rng.random() < 0.03:
            mid = {'start_stop': 1 - start_stop}
        if i >= 8 and rng.random() < 0.004:
            mid = {'reset': 1}
    return rows

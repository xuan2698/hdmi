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
        elif i < 10:
            reset = 0
            start_stop = 1
        else:
            reset = 0
            r = rng.random()
            if r < 0.015:
                start_stop = 1 - start_stop
            elif r < 0.03:
                start_stop = 1
            elif r < 0.045:
                start_stop = 0
            elif r < 0.05:
                reset = 1
        row = {'reset': reset, 'start_stop': start_stop}
        mid = {}
        if i >= 10 and rng.random() < 0.02:
            mid['start_stop'] = 1 - start_stop
        if i >= 10 and rng.random() < 0.005:
            mid['reset'] = 1
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows

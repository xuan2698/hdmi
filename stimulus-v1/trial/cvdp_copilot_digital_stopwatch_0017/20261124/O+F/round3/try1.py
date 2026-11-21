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
        elif i < 12:
            reset = 0
            start_stop = 1
        else:
            reset = 0
            r = rng.random()
            if r < 0.03:
                start_stop = 1 - start_stop
            elif r < 0.06:
                start_stop = 1
            elif r < 0.09:
                start_stop = 0
            elif r < 0.10:
                reset = 1
        row = {'reset': reset, 'start_stop': start_stop}
        mid = {}
        if i >= 12 and rng.random() < 0.015:
            mid['start_stop'] = 1 - start_stop
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows

def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i < 4:
            reset = 1
            start_stop = 0
        elif i < 6:
            reset = 0
            start_stop = 0
        else:
            reset = 0
            r = rng.random()
            if r < 0.04:
                start_stop = 1 - start_stop
            elif r < 0.08:
                start_stop = 1
            elif r < 0.12:
                start_stop = 0
            elif r < 0.14:
                reset = 1
        row = {'reset': reset, 'start_stop': start_stop}
        mid = {}
        if i >= 6 and rng.random() < 0.02:
            mid['start_stop'] = 1 - start_stop
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows

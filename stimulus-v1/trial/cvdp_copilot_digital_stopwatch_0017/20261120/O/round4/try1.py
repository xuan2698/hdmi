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
        elif i < 200:
            reset = 0
            start_stop = 1
        elif i < 210:
            reset = 0
            start_stop = 0
        elif i < 400:
            reset = 0
            start_stop = 1
        elif i < 410:
            reset = 0
            start_stop = 0
        elif i < 600:
            reset = 0
            start_stop = 1
        elif i < 610:
            reset = 0
            start_stop = 0
        elif i < 800:
            reset = 0
            start_stop = 1
        elif i < 810:
            reset = 0
            start_stop = 0
        elif i < 1000:
            reset = 0
            start_stop = 1
        elif i < 1010:
            reset = 0
            start_stop = 0
        elif i < 1200:
            reset = 0
            start_stop = 1
        elif i < 1210:
            reset = 0
            start_stop = 0
        elif i < 1400:
            reset = 0
            start_stop = 1
        elif i < 1410:
            reset = 0
            start_stop = 0
        elif i < 1600:
            reset = 0
            start_stop = 1
        elif i < 1610:
            reset = 0
            start_stop = 0
        elif i < 1800:
            reset = 0
            start_stop = 1
        elif i < 1810:
            reset = 0
            start_stop = 0
        elif i < 2000:
            reset = 0
            start_stop = 1
        elif i < 2010:
            reset = 0
            start_stop = 0
        elif i < 2200:
            reset = 0
            start_stop = 1
        elif i < 2210:
            reset = 0
            start_stop = 0
        elif i < 2400:
            reset = 0
            start_stop = 1
        elif i < 2410:
            reset = 0
            start_stop = 0
        elif i < 2600:
            reset = 0
            start_stop = 1
        elif i < 2610:
            reset = 0
            start_stop = 0
        elif i < 2800:
            reset = 0
            start_stop = 1
        elif i < 2810:
            reset = 0
            start_stop = 0
        elif i < 3000:
            reset = 0
            start_stop = 1
        elif i < 3010:
            reset = 0
            start_stop = 0
        elif i < 3200:
            reset = 0
            start_stop = 1
        elif i < 3210:
            reset = 0
            start_stop = 0
        elif i < 3400:
            reset = 0
            start_stop = 1
        elif i < 3410:
            reset = 0
            start_stop = 0
        elif i < 3600:
            reset = 0
            start_stop = 1
        elif i < 3610:
            reset = 0
            start_stop = 0
        elif i < 3800:
            reset = 0
            start_stop = 1
        elif i < 3810:
            reset = 0
            start_stop = 0
        elif i < 3980:
            reset = 0
            start_stop = 1
        else:
            reset = 0
            start_stop = 0
        row = {'reset': reset, 'start_stop': start_stop}
        if mid is not None:
            row['mid'] = mid
        rows.append(row)
        mid = None
        if i >= 8 and rng.random() < 0.03:
            mid = {'start_stop': 1 - start_stop}
    return rows

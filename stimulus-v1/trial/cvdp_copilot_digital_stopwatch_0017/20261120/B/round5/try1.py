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
            elif i < 40:
                start_stop = 1
            elif i < 44:
                start_stop = 0
            elif i < 200:
                start_stop = 1
            elif i < 204:
                start_stop = 0
            elif i < 600:
                start_stop = 1
            elif i < 604:
                start_stop = 0
            elif i < 1000:
                start_stop = 1
            elif i < 1004:
                start_stop = 0
            elif i < 1400:
                start_stop = 1
            elif i < 1404:
                start_stop = 0
            elif i < 1800:
                start_stop = 1
            elif i < 1804:
                start_stop = 0
            elif i < 2200:
                start_stop = 1
            elif i < 2204:
                start_stop = 0
            elif i < 2600:
                start_stop = 1
            elif i < 2604:
                start_stop = 0
            elif i < 3000:
                start_stop = 1
            elif i < 3004:
                start_stop = 0
            elif i < 3400:
                start_stop = 1
            elif i < 3404:
                start_stop = 0
            elif i < 3800:
                start_stop = 1
            else:
                r = rng.random()
                if r < 0.03:
                    start_stop = 1 - start_stop
                elif r < 0.04:
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

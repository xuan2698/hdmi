def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i < 2:
            reset = 1
            start_stop = 0
        elif i == 2:
            reset = 0
            start_stop = 0
        else:
            if i == 3:
                start_stop = 1
            elif i == 4:
                start_stop = 0
            elif i == 5:
                start_stop = 1
            elif i == 6:
                start_stop = 0
            elif i == 7:
                start_stop = 1
            elif i == 100:
                start_stop = 0
            elif i == 150:
                start_stop = 1
            elif i == 400:
                start_stop = 0
            elif i == 450:
                start_stop = 1
            elif i == 800:
                start_stop = 0
            elif i == 850:
                start_stop = 1
            elif i == 1200:
                start_stop = 0
            elif i == 1250:
                start_stop = 1
            elif i == 1600:
                start_stop = 0
            elif i == 1650:
                start_stop = 1
            elif i == 2000:
                start_stop = 0
            elif i == 2050:
                start_stop = 1
            elif i == 2400:
                start_stop = 0
            elif i == 2450:
                start_stop = 1
            elif i == 2800:
                start_stop = 0
            elif i == 2850:
                start_stop = 1
            elif i == 3200:
                start_stop = 0
            elif i == 3250:
                start_stop = 1
            elif i == 3600:
                start_stop = 0
            elif i == 3650:
                start_stop = 1
            elif rng.random() < 0.001:
                start_stop ^= 1
            if i == 500:
                reset = 1
            elif i == 502:
                reset = 0
            elif i == 1500:
                reset = 1
            elif i == 1502:
                reset = 0
            elif i == 2500:
                reset = 1
            elif i == 2502:
                reset = 0
            elif rng.random() < 0.0001:
                reset = 1
            elif reset == 1 and rng.random() < 0.5:
                reset = 0
        row = {'reset': reset, 'start_stop': start_stop}
        if i == 2:
            row['mid'] = {'start_stop': 0}
        elif i == 3:
            row['mid'] = {'start_stop': 0}
        elif i == 4:
            row['mid'] = {'start_stop': 1}
        elif i == 5:
            row['mid'] = {'start_stop': 0}
        elif i == 6:
            row['mid'] = {'start_stop': 1}
        rows.append(row)
    return rows

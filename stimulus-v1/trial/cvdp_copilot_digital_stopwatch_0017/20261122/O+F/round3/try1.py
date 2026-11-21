def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
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
                start_stop = 1
            elif i < 10:
                start_stop = 0
            elif i < 20:
                start_stop = 1
            elif i < 22:
                start_stop = 0
            elif i < 40:
                start_stop = 1
            elif i < 42:
                start_stop = 0
            elif i < 80:
                start_stop = 1
            elif i < 82:
                start_stop = 0
            elif i < 160:
                start_stop = 1
            elif i < 162:
                start_stop = 0
            elif i < 320:
                start_stop = 1
            elif i < 322:
                start_stop = 0
            elif i < 640:
                start_stop = 1
            elif i < 642:
                start_stop = 0
            elif i < 1280:
                start_stop = 1
            elif i < 1282:
                start_stop = 0
            elif i < 2560:
                start_stop = 1
            elif i < 2562:
                start_stop = 0
            elif i < 3800:
                start_stop = 1
            else:
                start_stop = 0
        row = {'reset': reset, 'start_stop': start_stop}
        if i == 6:
            row['mid'] = {'start_stop': 0}
        elif i == 18:
            row['mid'] = {'start_stop': 0}
        elif i == 38:
            row['mid'] = {'start_stop': 0}
        elif i == 78:
            row['mid'] = {'start_stop': 0}
        elif i == 158:
            row['mid'] = {'start_stop': 0}
        elif i == 318:
            row['mid'] = {'start_stop': 0}
        elif i == 638:
            row['mid'] = {'start_stop': 0}
        elif i == 1278:
            row['mid'] = {'start_stop': 0}
        elif i == 2558:
            row['mid'] = {'start_stop': 0}
        elif i == 3798:
            row['mid'] = {'start_stop': 0}
        rows.append(row)
    return rows

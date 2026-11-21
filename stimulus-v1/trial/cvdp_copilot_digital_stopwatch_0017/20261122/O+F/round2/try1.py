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
            reset = 0
            if i < 6:
                start_stop = 1
            elif i < 8:
                start_stop = 0
            elif i < 12:
                start_stop = 1
            elif i < 14:
                start_stop = 0
            elif i < 20:
                start_stop = 1
            elif i < 22:
                start_stop = 0
            elif i < 30:
                start_stop = 1
            elif i < 32:
                start_stop = 0
            elif i < 60:
                start_stop = 1
            elif i < 62:
                start_stop = 0
            elif i < 120:
                start_stop = 1
            elif i < 122:
                start_stop = 0
            elif i < 240:
                start_stop = 1
            elif i < 242:
                start_stop = 0
            elif i < 480:
                start_stop = 1
            elif i < 482:
                start_stop = 0
            elif i < 960:
                start_stop = 1
            elif i < 962:
                start_stop = 0
            elif i < 1920:
                start_stop = 1
            elif i < 1922:
                start_stop = 0
            elif i < 3840:
                start_stop = 1
            else:
                start_stop = 0
        row = {'reset': reset, 'start_stop': start_stop}
        if i == 4:
            row['mid'] = {'start_stop': 0}
        elif i == 10:
            row['mid'] = {'start_stop': 0}
        elif i == 18:
            row['mid'] = {'start_stop': 0}
        elif i == 28:
            row['mid'] = {'start_stop': 0}
        elif i == 58:
            row['mid'] = {'start_stop': 0}
        elif i == 118:
            row['mid'] = {'start_stop': 0}
        elif i == 238:
            row['mid'] = {'start_stop': 0}
        elif i == 478:
            row['mid'] = {'start_stop': 0}
        elif i == 958:
            row['mid'] = {'start_stop': 0}
        elif i == 1918:
            row['mid'] = {'start_stop': 0}
        elif i == 3838:
            row['mid'] = {'start_stop': 0}
        rows.append(row)
    return rows

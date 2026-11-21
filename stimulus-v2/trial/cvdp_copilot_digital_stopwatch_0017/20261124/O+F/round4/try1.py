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
            elif i == 5:
                start_stop = 0
            elif i == 6:
                start_stop = 1
            elif i == 8:
                start_stop = 0
            elif i == 9:
                start_stop = 1
            elif i == 12:
                start_stop = 0
            elif i == 13:
                start_stop = 1
            elif i == 20:
                start_stop = 0
            elif i == 21:
                start_stop = 1
            elif i == 40:
                start_stop = 0
            elif i == 41:
                start_stop = 1
            elif i == 100:
                start_stop = 0
            elif i == 101:
                start_stop = 1
            elif i == 300:
                start_stop = 0
            elif i == 301:
                start_stop = 1
            elif i == 700:
                start_stop = 0
            elif i == 701:
                start_stop = 1
            elif i == 1500:
                start_stop = 0
            elif i == 1501:
                start_stop = 1
            elif i == 2500:
                start_stop = 0
            elif i == 2501:
                start_stop = 1
            elif i == 3500:
                start_stop = 0
            elif i == 3501:
                start_stop = 1
            else:
                if rng.random() < 0.002:
                    start_stop = 1 - start_stop
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

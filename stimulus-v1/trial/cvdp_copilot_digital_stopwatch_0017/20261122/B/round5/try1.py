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
            elif i < 12:
                start_stop = 0
            elif i < 20:
                start_stop = 1
            elif i < 24:
                start_stop = 0
            elif i < 40:
                start_stop = 1
            elif i < 44:
                start_stop = 0
            elif i < 80:
                start_stop = 1
            elif i < 84:
                start_stop = 0
            elif i < 160:
                start_stop = 1
            elif i < 164:
                start_stop = 0
            elif i < 320:
                start_stop = 1
            elif i < 324:
                start_stop = 0
            elif i < 640:
                start_stop = 1
            elif i < 644:
                start_stop = 0
            elif i < 1280:
                start_stop = 1
            elif i < 1284:
                start_stop = 0
            elif i < 2560:
                start_stop = 1
            elif i < 2564:
                start_stop = 0
            elif i < 3000:
                start_stop = 1
            elif i < 3004:
                start_stop = 0
            elif i < 3500:
                start_stop = 1
            elif i < 3504:
                start_stop = 0
            else:
                start_stop = 1 if (i % 7) < 5 else 0
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

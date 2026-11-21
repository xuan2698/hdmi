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
            if i < 10:
                start_stop = 1
            elif i < 20:
                start_stop = 0
            elif i < 80:
                start_stop = 1
            elif i < 90:
                start_stop = 0
            elif i < 200:
                start_stop = 1
            elif i < 210:
                start_stop = 0
            elif i < 400:
                start_stop = 1
            elif i < 410:
                start_stop = 0
            elif i < 700:
                start_stop = 1
            elif i < 710:
                start_stop = 0
            elif i < 1100:
                start_stop = 1
            elif i < 1110:
                start_stop = 0
            elif i < 1600:
                start_stop = 1
            elif i < 1610:
                start_stop = 0
            elif i < 2200:
                start_stop = 1
            elif i < 2210:
                start_stop = 0
            elif i < 2900:
                start_stop = 1
            elif i < 2910:
                start_stop = 0
            elif i < 3600:
                start_stop = 1
            else:
                start_stop = 0
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

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
        elif i == 3:
            reset = 0
            start_stop = 1
        else:
            reset = 0
            if i < 40:
                start_stop = 1
            elif i < 60:
                start_stop = 0
            elif i < 200:
                start_stop = 1
            elif i < 210:
                start_stop = 0
            elif i < 400:
                start_stop = 1
            elif i < 410:
                start_stop = 0
            elif i < 800:
                start_stop = 1
            elif i < 810:
                start_stop = 0
            elif i < 1200:
                start_stop = 1
            elif i < 1210:
                start_stop = 0
            elif i < 1600:
                start_stop = 1
            elif i < 1610:
                start_stop = 0
            elif i < 2000:
                start_stop = 1
            elif i < 2010:
                start_stop = 0
            elif i < 2400:
                start_stop = 1
            elif i < 2410:
                start_stop = 0
            elif i < 2800:
                start_stop = 1
            elif i < 2810:
                start_stop = 0
            elif i < 3200:
                start_stop = 1
            elif i < 3210:
                start_stop = 0
            elif i < 3600:
                start_stop = 1
            elif i < 3610:
                start_stop = 0
            else:
                start_stop = 1
            if i % 500 == 250:
                reset = 1
            else:
                reset = 0
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

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
                start_stop = 0
            elif i < 20:
                start_stop = 1
            elif i < 30:
                start_stop = 0
            elif i < 200:
                start_stop = 1
            elif i < 210:
                start_stop = 0
            elif i < 400:
                start_stop = 1
            elif i < 410:
                start_stop = 0
            elif i < 600:
                start_stop = 1
            elif i < 610:
                start_stop = 0
            elif i < 800:
                start_stop = 1
            elif i < 810:
                start_stop = 0
            elif i < 1000:
                start_stop = 1
            elif i < 1010:
                start_stop = 0
            elif i < 1200:
                start_stop = 1
            elif i < 1210:
                start_stop = 0
            elif i < 1400:
                start_stop = 1
            elif i < 1410:
                start_stop = 0
            elif i < 1600:
                start_stop = 1
            elif i < 1610:
                start_stop = 0
            elif i < 1800:
                start_stop = 1
            elif i < 1810:
                start_stop = 0
            elif i < 2000:
                start_stop = 1
            elif i < 2010:
                start_stop = 0
            elif i < 2200:
                start_stop = 1
            elif i < 2210:
                start_stop = 0
            elif i < 2400:
                start_stop = 1
            elif i < 2410:
                start_stop = 0
            elif i < 2600:
                start_stop = 1
            elif i < 2610:
                start_stop = 0
            elif i < 2800:
                start_stop = 1
            elif i < 2810:
                start_stop = 0
            elif i < 3000:
                start_stop = 1
            elif i < 3010:
                start_stop = 0
            elif i < 3200:
                start_stop = 1
            elif i < 3210:
                start_stop = 0
            elif i < 3400:
                start_stop = 1
            elif i < 3410:
                start_stop = 0
            elif i < 3600:
                start_stop = 1
            elif i < 3610:
                start_stop = 0
            elif i < 3800:
                start_stop = 1
            elif i < 3810:
                start_stop = 0
            else:
                start_stop = 1
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

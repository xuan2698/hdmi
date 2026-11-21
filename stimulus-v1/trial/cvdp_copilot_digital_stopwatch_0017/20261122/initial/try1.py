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
            elif i < 40:
                start_stop = 1
            elif i < 50:
                start_stop = 0
            elif i < 100:
                start_stop = 1
            elif i < 120:
                start_stop = 0
            elif i < 200:
                start_stop = 1
            elif i < 220:
                start_stop = 0
            elif i < 400:
                start_stop = 1
            elif i < 420:
                start_stop = 0
            elif i < 800:
                start_stop = 1
            elif i < 820:
                start_stop = 0
            elif i < 1200:
                start_stop = 1
            elif i < 1220:
                start_stop = 0
            elif i < 1600:
                start_stop = 1
            elif i < 1620:
                start_stop = 0
            elif i < 2000:
                start_stop = 1
            elif i < 2020:
                start_stop = 0
            elif i < 2400:
                start_stop = 1
            elif i < 2420:
                start_stop = 0
            elif i < 2800:
                start_stop = 1
            elif i < 2820:
                start_stop = 0
            elif i < 3200:
                start_stop = 1
            elif i < 3220:
                start_stop = 0
            elif i < 3600:
                start_stop = 1
            elif i < 3620:
                start_stop = 0
            elif i < 3960:
                start_stop = 1
            else:
                start_stop = 0
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

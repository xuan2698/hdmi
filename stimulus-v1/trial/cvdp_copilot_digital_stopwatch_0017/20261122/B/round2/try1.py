def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i < 4:
            reset = 1
            start_stop = 0
        elif i == 4:
            reset = 0
            start_stop = 0
        else:
            reset = 0
            if i < 12:
                start_stop = 1
            elif i < 24:
                start_stop = 0
            elif i < 60:
                start_stop = 1
            elif i < 72:
                start_stop = 0
            elif i < 140:
                start_stop = 1
            elif i < 152:
                start_stop = 0
            elif i < 260:
                start_stop = 1
            elif i < 272:
                start_stop = 0
            elif i < 420:
                start_stop = 1
            elif i < 432:
                start_stop = 0
            elif i < 620:
                start_stop = 1
            elif i < 632:
                start_stop = 0
            elif i < 860:
                start_stop = 1
            elif i < 872:
                start_stop = 0
            elif i < 1140:
                start_stop = 1
            elif i < 1152:
                start_stop = 0
            elif i < 1460:
                start_stop = 1
            elif i < 1472:
                start_stop = 0
            elif i < 1820:
                start_stop = 1
            elif i < 1832:
                start_stop = 0
            elif i < 2220:
                start_stop = 1
            elif i < 2232:
                start_stop = 0
            elif i < 2660:
                start_stop = 1
            elif i < 2672:
                start_stop = 0
            elif i < 3140:
                start_stop = 1
            elif i < 3152:
                start_stop = 0
            elif i < 3660:
                start_stop = 1
            else:
                start_stop = 0
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

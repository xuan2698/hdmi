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
            elif i < 20:
                start_stop = 0
            elif i < 60:
                start_stop = 1
            elif i < 70:
                start_stop = 0
            elif i < 130:
                start_stop = 1
            elif i < 140:
                start_stop = 0
            elif i < 220:
                start_stop = 1
            elif i < 230:
                start_stop = 0
            elif i < 330:
                start_stop = 1
            elif i < 340:
                start_stop = 0
            elif i < 470:
                start_stop = 1
            elif i < 480:
                start_stop = 0
            elif i < 640:
                start_stop = 1
            elif i < 650:
                start_stop = 0
            elif i < 850:
                start_stop = 1
            elif i < 860:
                start_stop = 0
            elif i < 1100:
                start_stop = 1
            elif i < 1110:
                start_stop = 0
            elif i < 1400:
                start_stop = 1
            elif i < 1410:
                start_stop = 0
            elif i < 1750:
                start_stop = 1
            elif i < 1760:
                start_stop = 0
            elif i < 2150:
                start_stop = 1
            elif i < 2160:
                start_stop = 0
            elif i < 2600:
                start_stop = 1
            elif i < 2610:
                start_stop = 0
            elif i < 3100:
                start_stop = 1
            elif i < 3110:
                start_stop = 0
            elif i < 3600:
                start_stop = 1
            else:
                start_stop = 0
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

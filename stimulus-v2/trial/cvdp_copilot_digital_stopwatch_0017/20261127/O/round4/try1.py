def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i == 0:
            reset = 1
            start_stop = 0
        elif i == 2:
            reset = 0
            start_stop = 0
        elif i == 4:
            start_stop = 1
        elif i == 300:
            start_stop = 0
        elif i == 320:
            start_stop = 1
        elif i == 600:
            reset = 1
        elif i == 602:
            reset = 0
            start_stop = 0
        elif i == 604:
            start_stop = 1
        elif i == 1200:
            start_stop = 0
        elif i == 1250:
            start_stop = 1
        elif i == 2000:
            reset = 1
        elif i == 2002:
            reset = 0
            start_stop = 1
        elif i == 2600:
            start_stop = 0
        elif i == 2700:
            start_stop = 1
        elif i == 3200:
            reset = 1
        elif i == 3202:
            reset = 0
            start_stop = 0
        elif i == 3205:
            start_stop = 1
        elif i == 3600:
            start_stop = 0
        elif i == 3650:
            start_stop = 1
        elif i == 3900:
            reset = 1
        elif i == 3902:
            reset = 0
            start_stop = 1
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

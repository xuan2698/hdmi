def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i == 2:
            reset = 0
        if i == 4:
            start_stop = 1
        if i == 300:
            start_stop = 0
        if i == 400:
            start_stop = 1
        if i == 1200:
            reset = 1
        if i == 1202:
            reset = 0
        if i == 1300:
            start_stop = 0
        if i == 1400:
            start_stop = 1
        if i == 2500:
            start_stop = 0
        if i == 2600:
            start_stop = 1
        if i == 3500:
            reset = 1
        if i == 3502:
            reset = 0
        if i == 3600:
            start_stop = 0
        if i == 3700:
            start_stop = 1
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

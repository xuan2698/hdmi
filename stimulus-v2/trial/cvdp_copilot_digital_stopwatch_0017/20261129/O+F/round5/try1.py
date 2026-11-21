def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i == 2:
            reset = 0
        if i == 4:
            start_stop = 1
        if i == 60:
            start_stop = 0
        if i == 80:
            start_stop = 1
        if i == 400:
            reset = 1
        if i == 402:
            reset = 0
        if i == 404:
            start_stop = 1
        if i == 900:
            start_stop = 0
        if i == 950:
            start_stop = 1
        if i == 1500:
            reset = 1
        if i == 1502:
            reset = 0
        if i == 1504:
            start_stop = 1
        if i == 2200:
            start_stop = 0
        if i == 2250:
            start_stop = 1
        if i == 3000:
            reset = 1
        if i == 3002:
            reset = 0
        if i == 3004:
            start_stop = 1
        if i == 3600:
            start_stop = 0
        if i == 3650:
            start_stop = 1
        row = {'reset': reset, 'start_stop': start_stop}
        rows.append(row)
    return rows

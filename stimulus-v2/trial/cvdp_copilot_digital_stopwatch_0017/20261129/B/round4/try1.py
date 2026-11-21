def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i == 3:
            reset = 0
        if i == 5:
            start_stop = 1
        if i == 200:
            start_stop = 0
        if i == 250:
            start_stop = 1
        if i == 5000:
            reset = 1
        if i == 5003:
            reset = 0
        if i == 5005:
            start_stop = 1
        if i == 12000:
            start_stop = 0
        if i == 12050:
            start_stop = 1
        if i == 18000:
            reset = 1
        if i == 18003:
            reset = 0
        if i == 18005:
            start_stop = 1
        if i == 24000:
            start_stop = 0
        if i == 24050:
            start_stop = 1
        if i == 30000:
            reset = 1
        if i == 30003:
            reset = 0
        if i == 30005:
            start_stop = 1
        if i == 36000:
            start_stop = 0
        if i == 36050:
            start_stop = 1
        row = {'reset': reset, 'start_stop': start_stop}
        rows.append(row)
    return rows

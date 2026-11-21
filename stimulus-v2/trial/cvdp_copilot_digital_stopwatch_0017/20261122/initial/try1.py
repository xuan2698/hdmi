def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i == 3:
            reset = 0
        if i == 5:
            start_stop = 1
        if i == 500:
            start_stop = 0
        if i == 600:
            start_stop = 1
        if i == 1500:
            reset = 1
        if i == 1503:
            reset = 0
        if i == 1600:
            start_stop = 0
        if i == 1700:
            start_stop = 1
        if i == 5000:
            start_stop = 0
        if i == 5100:
            start_stop = 1
        if i == 10000:
            reset = 1
        if i == 10003:
            reset = 0
        if i == 10100:
            start_stop = 0
        if i == 10200:
            start_stop = 1
        if i == 15000:
            start_stop = 0
        if i == 15100:
            start_stop = 1
        if i == 19000:
            reset = 1
        if i == 19003:
            reset = 0
        if i == 19100:
            start_stop = 0
        if i == 19200:
            start_stop = 1
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

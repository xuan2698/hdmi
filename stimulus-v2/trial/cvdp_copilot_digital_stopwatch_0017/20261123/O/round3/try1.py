def stimulus(rng, cycles):
    rows = []
    reset = 1
    start_stop = 0
    for i in range(cycles):
        if i == 0:
            reset = 1
            start_stop = 0
        elif i == 3:
            reset = 0
            start_stop = 0
        elif i == 5:
            start_stop = 1
        elif i == 5000:
            start_stop = 0
        elif i == 5100:
            start_stop = 1
        elif i == 12000:
            reset = 1
        elif i == 12003:
            reset = 0
            start_stop = 0
        elif i == 12005:
            start_stop = 1
        elif i == 18000:
            start_stop = 0
        elif i == 18100:
            start_stop = 1
        elif i == 25000:
            start_stop = 0
        elif i == 25100:
            start_stop = 1
        elif i == 32000:
            reset = 1
        elif i == 32003:
            reset = 0
            start_stop = 0
        elif i == 32005:
            start_stop = 1
        elif i == 38000:
            start_stop = 0
        elif i == 38100:
            start_stop = 1
        rows.append({'reset': reset, 'start_stop': start_stop})
    return rows

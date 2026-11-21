def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i < 6:
            reset = 0
        elif i < 10:
            reset = 1
        elif i < 50:
            reset = 0
        elif i < 53:
            reset = 1
        elif i < 60:
            reset = 0
        elif i < 62:
            reset = 1
        elif i < 200:
            reset = 0
        elif i < 203:
            reset = 1
        elif i < 260:
            reset = 0
        elif i < 262:
            reset = 1
        elif i < 400:
            reset = 0
        elif i < 402:
            reset = 1
        elif i < 1000:
            reset = 0
        elif i < 1003:
            reset = 1
        elif i < 1200:
            reset = 0
        elif i < 1202:
            reset = 1
        elif i < 2000:
            reset = 0
        elif i < 2003:
            reset = 1
        elif i < 2400:
            reset = 0
        elif i < 2402:
            reset = 1
        elif i < 3000:
            reset = 0
        elif i < 3003:
            reset = 1
        elif i < 3400:
            reset = 0
        elif i < 3402:
            reset = 1
        else:
            reset = 0
        row = {'reset': reset}
        rows.append(row)
    return rows

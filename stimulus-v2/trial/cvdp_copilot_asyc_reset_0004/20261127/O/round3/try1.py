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
        elif i < 12:
            reset = 0
        elif i < 14:
            reset = 1
        elif i < 20:
            reset = 0
        elif i < 22:
            reset = 1
        elif i < 60:
            reset = 0
        elif i < 62:
            reset = 1
        elif i < 200:
            reset = 0
        elif i < 202:
            reset = 1
        elif i < 500:
            reset = 0
        elif i < 502:
            reset = 1
        elif i < 1000:
            reset = 0
        elif i < 1002:
            reset = 1
        elif i < 2000:
            reset = 0
        elif i < 2002:
            reset = 1
        elif i < 3000:
            reset = 0
        elif i < 3002:
            reset = 1
        else:
            reset = 0
        row = {'reset': reset}
        rows.append(row)
    return rows

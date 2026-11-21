def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 2:
            reset = 1
        elif i < 4:
            reset = 0
        elif i < 6:
            reset = 1
        elif i < 8:
            reset = 0
        elif i < 10:
            reset = 1
        elif i < 40:
            reset = 0
        elif i < 42:
            reset = 1
        elif i < 80:
            reset = 0
        elif i < 82:
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
        rows.append({'reset': reset})
    return rows

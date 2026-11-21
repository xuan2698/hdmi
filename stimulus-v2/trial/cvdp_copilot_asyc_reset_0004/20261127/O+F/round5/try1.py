def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i < 35:
            reset = 0
        elif i < 37:
            reset = 1
        elif i < 90:
            reset = 0
        elif i < 91:
            reset = 1
        elif i < 150:
            reset = 0
        elif i < 152:
            reset = 1
        elif i < 300:
            reset = 0
        elif i < 301:
            reset = 1
        elif i < 500:
            reset = 0
        elif i < 502:
            reset = 1
        elif i < 1000:
            reset = 0
        elif i < 1001:
            reset = 1
        elif i < 2000:
            reset = 0
        elif i < 2002:
            reset = 1
        elif i < 3000:
            reset = 0
        elif i < 3001:
            reset = 1
        else:
            reset = 0
        rows.append({'reset': reset})
    return rows

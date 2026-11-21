def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i == 3:
            reset = 0
        elif i == 1000:
            reset = 1
        elif i == 1003:
            reset = 0
        elif i == 5000:
            reset = 1
        elif i == 5002:
            reset = 0
        elif i == 12000:
            reset = 1
        elif i == 12001:
            reset = 0
        elif i == 20000:
            reset = 1
        elif i == 20001:
            reset = 0
        elif i == 30000:
            reset = 1
        elif i == 30002:
            reset = 0
        elif i == 35000:
            reset = 1
        elif i == 35001:
            reset = 0
        elif i == 38000:
            reset = 1
        elif i == 38005:
            reset = 0
        rows.append({'reset': reset})
    return rows

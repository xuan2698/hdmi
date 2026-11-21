def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(20000):
        if i < 3:
            reset = 1
        elif i < 5:
            reset = 0
        elif i == 5:
            reset = 1
        elif i < 8:
            reset = 0
        else:
            reset = 0
        rows.append({'reset': reset})
    return rows

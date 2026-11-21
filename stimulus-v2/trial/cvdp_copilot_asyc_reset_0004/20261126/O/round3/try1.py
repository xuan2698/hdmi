def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(4000):
        if i < 2:
            reset = 1
        elif i < 4:
            reset = 0
        elif i == 4:
            reset = 1
        elif i < 7:
            reset = 0
        else:
            reset = 0
        rows.append({'reset': reset})
    return rows

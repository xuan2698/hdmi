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
        else:
            reset = 0
        rows.append({'reset': reset})
    return rows

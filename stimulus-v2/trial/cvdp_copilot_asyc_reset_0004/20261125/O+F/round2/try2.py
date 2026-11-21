def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 3:
            reset = 1
        elif i == 3:
            reset = 0
        elif i == 15000:
            reset = 1
        elif i == 15003:
            reset = 0
        elif i == 30000:
            reset = 1
        elif i == 30002:
            reset = 0
        elif i == 45000:
            reset = 1
        elif i == 45001:
            reset = 0
        row = {'reset': reset}
        rows.append(row)
    return rows

def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
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
        row = {'reset': reset}
        if i == 5:
            row['mid'] = {'reset': 0}
        rows.append(row)
    return rows

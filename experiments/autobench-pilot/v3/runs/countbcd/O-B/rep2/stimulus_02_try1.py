def stimulus(rng, cycles):
    rows = []
    q = 0
    for i in range(cycles):
        if i < 8:
            reset = 1 if i < 2 else 0
        else:
            reset = 0
        rows.append({'reset': reset})
    return rows

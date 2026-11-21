def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        r = {"reset": 1 if i < 2 else 0}
        if i >= 2 and i % 7 == 0:
            r["reset"] = 1
        rows.append(r)
    return rows

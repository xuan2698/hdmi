def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    for i in range(cycles - 2):
        if i < 4:
            rows.append({'reset': 0})
        else:
            r = rng.randrange(4)
            if r == 0:
                rows.append({'reset': 1})
            else:
                rows.append({'reset': 0})
    return rows[:cycles]

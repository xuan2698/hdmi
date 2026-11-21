def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    for i in range(cycles - 2):
        r = 0
        if i < 4:
            r = 1 if i == 0 else 0
        else:
            r = 1 if rng.randrange(20) == 0 else 0
        rows.append({'reset': r})
    return rows[:cycles]

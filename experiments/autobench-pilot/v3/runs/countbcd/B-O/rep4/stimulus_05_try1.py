def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    for i in range(cycles - 2):
        if i < 4:
            rows.append({'reset': 0})
        else:
            rows.append({'reset': 1 if rng.randrange(20) == 0 else 0})
    return rows[:cycles]

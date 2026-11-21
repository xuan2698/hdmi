def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    for _ in range(cycles - 2):
        rows.append({'reset': 0})
    return rows[:cycles]

def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    for i in range(cycles - 2):
        if i < 10:
            rows.append({'reset': 0})
        else:
            rows.append({'reset': 0, 'mid': {'reset': rng.choice([0, 0, 0, 1])}})
    return rows[:cycles]

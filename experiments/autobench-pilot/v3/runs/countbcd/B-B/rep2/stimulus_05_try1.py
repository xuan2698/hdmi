def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    for _ in range(cycles - 2):
        r = rng.randrange(100)
        if r < 10:
            rows.append({'reset': 1})
        elif r < 20:
            rows.append({'reset': 0, 'mid': {'reset': 1}})
        else:
            rows.append({'reset': 0})
    return rows[:cycles]

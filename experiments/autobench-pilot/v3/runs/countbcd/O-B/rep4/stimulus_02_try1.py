def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    for i in range(cycles - 2):
        if i < 8:
            rows.append({'reset': 0})
        else:
            rows.append({'reset': rng.getrandbits(1) if rng.random() < 0.1 else 0})
    return rows[:cycles]

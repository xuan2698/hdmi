def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1})
    rows.append({'reset': 0})
    for i in range(cycles - 2):
        if i < 6:
            rows.append({'reset': 0})
        else:
            rows.append({'reset': rng.getrandbits(1)})
    return rows[:cycles]

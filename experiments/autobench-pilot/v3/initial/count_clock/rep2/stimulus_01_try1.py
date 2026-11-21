def stimulus(rng, cycles):
    rows = []
    rows.append({'reset': 1, 'ena': 0})
    rows.append({'reset': 0, 'ena': 0})
    rows.append({'reset': 0, 'ena': 1})
    for i in range(cycles - 3):
        r = rng.randrange(100)
        if r < 5:
            rows.append({'reset': 1, 'ena': rng.getrandbits(1)})
        elif r < 15:
            rows.append({'reset': 0, 'ena': 0})
        else:
            rows.append({'reset': 0, 'ena': 1})
    return rows[:cycles]

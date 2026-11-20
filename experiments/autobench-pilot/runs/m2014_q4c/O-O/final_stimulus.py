def stimulus(rng, cycles):
    fixed = [
        (0, 1), (1, 1), (0, 0), (1, 0), (0, 0), (1, 0), (0, 0), (1, 0),
        (0, 1), (1, 1), (0, 0), (1, 0), (1, 0), (0, 0), (0, 1), (1, 1),
        (0, 0), (1, 0), (0, 0), (1, 0), (0, 1), (1, 1), (0, 0), (1, 0)
    ]
    rows = []
    for i in range(cycles):
        if i < len(fixed):
            d, r = fixed[i]
        else:
            d = rng.getrandbits(1)
            if i % 9 == 0 or i % 13 == 0:
                r = 1
            else:
                r = rng.getrandbits(1)
        rows.append({'d': int(d), 'r': int(r)})
    return rows

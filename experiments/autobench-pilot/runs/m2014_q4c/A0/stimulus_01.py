def stimulus(rng, cycles):
    pattern = [
        (0, 1),
        (1, 0),
        (0, 0),
        (1, 0),
        (1, 0),
        (0, 0),
        (1, 1),
        (1, 0),
        (0, 1),
        (1, 0),
        (0, 0),
        (1, 1),
        (0, 0),
        (1, 0),
        (0, 0),
        (1, 0)
    ]
    rows = []
    n = len(pattern)
    for i in range(cycles):
        if i < n:
            d, r = pattern[i]
        else:
            r = 1 if rng.randrange(16) == 0 else 0
            d = rng.getrandbits(1)
        rows.append({"d": int(d), "r": int(r)})
    return rows

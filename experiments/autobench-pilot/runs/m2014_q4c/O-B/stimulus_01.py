def stimulus(rng, cycles):
    pattern = [
        (0, 1),
        (0, 1),
        (1, 1),
        (0, 0),
        (1, 0),
        (1, 0),
        (0, 0),
        (1, 1),
        (1, 0),
        (0, 0),
        (0, 1),
        (1, 1),
    ]
    out = []
    for i in range(cycles):
        if i < len(pattern):
            d, r = pattern[i]
        else:
            r = 1 if rng.randrange(5) == 0 else 0
            d = rng.getrandbits(1)
        out.append({'d': d, 'r': r})
    return out

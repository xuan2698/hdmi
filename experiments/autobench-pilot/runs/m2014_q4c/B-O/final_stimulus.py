def stimulus(rng, cycles):
    out = []
    if cycles <= 0:
        return out
    out.append({"d": 0, "r": 1})
    pattern = [
        (1, 0), (1, 0), (0, 0), (0, 0), (1, 1), (1, 0), (0, 1), (0, 0),
        (1, 1), (0, 0), (1, 0), (0, 1), (1, 0), (1, 0), (0, 1), (1, 1),
        (0, 0), (1, 0), (0, 1), (1, 0), (1, 1), (0, 0), (1, 1), (0, 1),
        (1, 0)
    ]
    i = 1
    j = 0
    while i < cycles and j < len(pattern):
        d, r = pattern[j]
        out.append({"d": d, "r": r})
        i += 1
        j += 1
    while i < cycles:
        if i % 11 == 0:
            d = rng.getrandbits(1)
            r = 1
        elif i % 7 == 0:
            d = 0
            r = 1
        elif i % 5 == 0:
            d = 1
            r = 0
        elif i % 3 == 0:
            d = 0
            r = 0
        else:
            d = rng.getrandbits(1)
            if rng.random() < 0.25:
                r = 1
            else:
                r = 0
        out.append({"d": d, "r": r})
        i += 1
    return out

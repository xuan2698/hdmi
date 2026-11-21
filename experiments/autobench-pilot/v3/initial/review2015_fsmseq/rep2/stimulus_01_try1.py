def stimulus(rng, cycles):
    rows = []
    seq = [1, 1, 0, 1]
    for i in range(cycles):
        r = {}
        r['reset'] = 1 if i < 2 else 0
        if i < 2:
            r['data'] = rng.getrandbits(1)
        elif i < 20:
            r['data'] = seq[(i - 2) % 4]
        elif i < 30:
            r['data'] = rng.choice([0, 1])
        elif i < 40:
            r['data'] = 1 if (i % 5) in (0, 1, 3) else 0
        else:
            r['data'] = rng.getrandbits(1)
        if i % 7 == 3 and i > 5:
            r['mid'] = {'data': rng.getrandbits(1)}
        rows.append(r)
    return rows

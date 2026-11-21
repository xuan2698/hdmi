def stimulus(rng, cycles):
    rows = []
    seq = [1, 1, 0, 1]
    for i in range(cycles):
        r = {}
        if i < 8:
            r['reset'] = 1 if i in (0, 4) else 0
            r['data'] = seq[i % 4]
        elif i < 16:
            r['reset'] = 0
            r['data'] = seq[(i - 8) % 4]
            if i == 12:
                r['mid'] = {'data': 0}
        else:
            r['reset'] = 1 if rng.randrange(20) == 0 else 0
            r['data'] = rng.getrandbits(1)
            if rng.randrange(4) == 0:
                r['mid'] = {'data': rng.getrandbits(1)}
        rows.append(r)
    return rows

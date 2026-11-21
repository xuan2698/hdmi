def stimulus(rng, cycles):
    rows = []
    seq = [1, 1, 0, 1]
    for i in range(cycles):
        r = {}
        if i == 0:
            r['reset'] = 1
            r['data'] = 0
        elif i == 1:
            r['reset'] = 0
            r['data'] = 1
        elif i < 8:
            r['reset'] = 0
            r['data'] = seq[(i - 2) % 4]
        else:
            r['reset'] = 1 if rng.randrange(20) == 0 else 0
            r['data'] = rng.getrandbits(1)
        if i % 5 == 3:
            r['mid'] = {'data': rng.getrandbits(1)}
        rows.append(r)
    return rows

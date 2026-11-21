def stimulus(rng, cycles):
    rows = []
    seq = [1, 1, 0, 1]
    for i in range(cycles):
        r = {}
        if i < 4:
            r['reset'] = 1 if i == 0 else 0
            r['data'] = seq[i]
        elif i < 8:
            r['reset'] = 0
            r['data'] = rng.getrandbits(1)
        elif i < 12:
            r['reset'] = 0
            r['data'] = seq[(i - 8) % 4]
        elif i < 16:
            r['reset'] = 1 if i == 12 else 0
            r['data'] = rng.getrandbits(1)
        else:
            r['reset'] = 0
            r['data'] = rng.getrandbits(1)
        if i % 5 == 2 and i < cycles - 1:
            r['mid'] = {'data': rng.getrandbits(1)}
        rows.append(r)
    return rows

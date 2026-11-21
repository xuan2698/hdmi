def stimulus(rng, cycles):
    rows = []
    seq = [1, 1, 0, 1]
    for i in range(cycles):
        r = {}
        r['reset'] = 1 if i == 0 else 0
        if i < 8:
            r['data'] = seq[i % 4]
        elif i < 12:
            r['data'] = rng.getrandbits(1)
        elif i < 16:
            r['data'] = 1
        else:
            r['data'] = rng.choice([0, 1])
        if i in (3, 7, 11, 15) and i + 1 < cycles:
            r['mid'] = {'data': rng.getrandbits(1)}
        rows.append(r)
    return rows

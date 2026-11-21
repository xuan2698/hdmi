def stimulus(rng, cycles):
    rows = []
    def row(bl=0, br=0, g=1, d=0, mid=None):
        r = {'areset': 0, 'bump_left': bl, 'bump_right': br, 'ground': g, 'dig': d}
        if mid is not None:
            r['mid'] = mid
        rows.append(r)
    row(0,0,1,0)
    row(0,0,1,1)
    row(0,0,1,0)
    row(0,0,0,0)
    row(0,0,0,0)
    row(0,0,1,0)
    row(1,0,1,0)
    row(0,1,1,0)
    row(1,1,1,0)
    row(0,0,1,1)
    row(0,0,0,0)
    row(0,0,1,0)
    row(0,0,1,0, {'ground':0})
    row(0,0,1,0)
    row(0,0,0,0)
    row(0,0,1,0)
    while len(rows) < cycles:
        bl = rng.getrandbits(1)
        br = rng.getrandbits(1)
        g = rng.getrandbits(1)
        d = rng.getrandbits(1)
        mid = None
        if rng.randrange(4) == 0:
            mid = {'ground': rng.getrandbits(1)}
        rows.append({'areset': 0, 'bump_left': bl, 'bump_right': br, 'ground': g, 'dig': d, **({'mid': mid} if mid else {})})
    return rows[:cycles]

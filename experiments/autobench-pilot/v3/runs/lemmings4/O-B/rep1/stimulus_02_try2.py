def stimulus(rng, cycles):
    rows = []
    def row(areset=0, bl=0, br=0, g=1, d=0, mid=None):
        r = {'areset': areset, 'bump_left': bl, 'bump_right': br, 'ground': g, 'dig': d}
        if mid is not None:
            r['mid'] = mid
        rows.append(r)
    row(areset=1)
    row(bl=1, br=0, g=1, d=0)
    row(bl=0, br=1, g=1, d=0)
    row(bl=1, br=1, g=1, d=0)
    row(bl=0, br=0, g=0, d=0)
    row(bl=1, br=1, g=0, d=1)
    row(bl=0, br=0, g=1, d=0)
    row(bl=0, br=0, g=1, d=1)
    row(bl=1, br=0, g=1, d=1)
    row(bl=0, br=0, g=0, d=0)
    row(bl=0, br=0, g=1, d=0)
    row(bl=0, br=0, g=0, d=0)
    row(bl=0, br=0, g=0, d=0)
    row(bl=0, br=0, g=0, d=0)
    row(bl=0, br=0, g=0, d=0)
    row(bl=0, br=0, g=0, d=0)
    while len(rows) < cycles:
        bl = rng.getrandbits(1)
        br = rng.getrandbits(1)
        g = rng.getrandbits(1)
        d = rng.getrandbits(1)
        mid = None
        if rng.randrange(4) == 0:
            mid = {'ground': rng.getrandbits(1)}
        rows.append({'areset': 0, 'bump_left': bl, 'bump_right': br, 'ground': g, 'dig': d, 'mid': mid} if mid else {'areset': 0, 'bump_left': bl, 'bump_right': br, 'ground': g, 'dig': d})
    return rows[:cycles]

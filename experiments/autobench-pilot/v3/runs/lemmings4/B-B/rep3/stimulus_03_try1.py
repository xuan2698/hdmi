def stimulus(rng, cycles):
    rows = []
    def row(**kw):
        d = {k: 0 for k in ('areset','bump_left','bump_right','ground','dig')}
        d.update(kw)
        rows.append(d)
    row(areset=1, ground=1)
    row(ground=1)
    row(ground=1, bump_left=1)
    row(ground=1, bump_right=1)
    row(ground=1, bump_left=1, bump_right=1)
    row(ground=1, dig=1)
    row(ground=0)
    row(ground=0, bump_left=1)
    row(ground=1)
    row(ground=1, dig=1)
    row(ground=0)
    row(ground=0)
    row(ground=1)
    row(ground=1, bump_right=1)
    row(ground=0, dig=1)
    row(ground=1)
    while len(rows) < cycles:
        g = rng.getrandbits(1)
        d = {
            'areset': 1 if rng.randrange(50) == 0 else 0,
            'bump_left': rng.getrandbits(1) if rng.randrange(3) == 0 else 0,
            'bump_right': rng.getrandbits(1) if rng.randrange(3) == 0 else 0,
            'ground': g,
            'dig': rng.getrandbits(1) if rng.randrange(4) == 0 else 0,
        }
        if rng.randrange(4) == 0:
            d['mid'] = {'ground': rng.getrandbits(1)}
        rows.append(d)
    return rows[:cycles]

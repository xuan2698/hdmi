def stimulus(rng, cycles):
    rows = []
    def r(**kw):
        d = {'areset': 0, 'bump_left': 0, 'bump_right': 0, 'ground': 1, 'dig': 0}
        d.update(kw)
        return d
    rows.append(r(areset=1))
    rows.append(r())
    rows.append(r(bump_left=1))
    rows.append(r(bump_right=1))
    rows.append(r(bump_left=1, bump_right=1))
    rows.append(r(ground=0))
    rows.append(r(ground=0, bump_left=1))
    rows.append(r(ground=1))
    rows.append(r(dig=1))
    rows.append(r(dig=1, ground=0))
    rows.append(r(ground=0))
    rows.append(r(ground=0))
    rows.append(r(ground=1, dig=1))
    rows.append(r(bump_left=1, dig=1))
    rows.append(r(ground=0, dig=1, bump_right=1))
    rows.append(r(ground=1))
    while len(rows) < cycles:
        d = r(
            areset=1 if rng.randrange(100) < 2 else 0,
            bump_left=rng.getrandbits(1),
            bump_right=rng.getrandbits(1),
            ground=rng.getrandbits(1),
            dig=rng.getrandbits(1),
        )
        if rng.randrange(100) < 30:
            d['mid'] = {'ground': rng.getrandbits(1)}
        rows.append(d)
    return rows[:cycles]

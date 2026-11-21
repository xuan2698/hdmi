def stimulus(rng, cycles):
    rows = []
    def row(areset=0, bump_left=0, bump_right=0, ground=1, dig=0, mid=None):
        d = {'areset': areset, 'bump_left': bump_left, 'bump_right': bump_right, 'ground': ground, 'dig': dig}
        if mid is not None:
            d['mid'] = mid
        rows.append(d)
    row(areset=1)
    row()
    row(bump_left=1)
    row(bump_right=1)
    row(bump_left=1, bump_right=1)
    row(ground=0)
    row(ground=0, bump_left=1)
    row(ground=1)
    row(dig=1)
    row(dig=1, ground=0)
    row(ground=0)
    row(ground=1)
    row(ground=0, mid={'ground': 1})
    row(ground=1, mid={'ground': 0})
    row(ground=0)
    row(ground=0)
    while len(rows) < cycles:
        r = rng.randrange(8)
        if r == 0:
            row(areset=1)
        elif r == 1:
            row(bump_left=rng.getrandbits(1), bump_right=rng.getrandbits(1))
        elif r == 2:
            row(ground=0)
        elif r == 3:
            row(ground=1, dig=rng.getrandbits(1))
        elif r == 4:
            row(ground=0, mid={'ground': 1})
        elif r == 5:
            row(ground=1, mid={'ground': 0})
        elif r == 6:
            row(bump_left=1, bump_right=1, ground=rng.getrandbits(1))
        else:
            row(ground=rng.getrandbits(1), dig=rng.getrandbits(1), bump_left=rng.getrandbits(1), bump_right=rng.getrandbits(1))
    return rows[:cycles]

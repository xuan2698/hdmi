def stimulus(rng, cycles):
    rows = []
    def add(areset=0, bump_left=0, bump_right=0, ground=1, dig=0, mid=None):
        r = {'areset': areset, 'bump_left': bump_left, 'bump_right': bump_right,
             'ground': ground, 'dig': dig}
        if mid is not None:
            r['mid'] = mid
        rows.append(r)
    add(areset=1)
    add()
    add(bump_left=1)
    add(bump_right=1)
    add(bump_left=1, bump_right=1)
    add(ground=0)
    add(ground=0, bump_left=1)
    add(ground=1)
    add(dig=1)
    add(dig=1)
    add(ground=0)
    add(ground=0)
    add(ground=1)
    add(ground=0)
    for _ in range(21):
        add(ground=0)
    add(ground=1)
    add()
    add(areset=1)
    add()
    while len(rows) < cycles:
        g = rng.getrandbits(1)
        bl = rng.getrandbits(1)
        br = rng.getrandbits(1)
        d = rng.getrandbits(1)
        ar = 1 if rng.randrange(100) < 2 else 0
        mid = None
        if rng.randrange(4) == 0:
            mid = {'ground': rng.getrandbits(1)}
        add(areset=ar, bump_left=bl, bump_right=br, ground=g, dig=d, mid=mid)
    return rows[:cycles]

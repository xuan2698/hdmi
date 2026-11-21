def stimulus(rng, cycles):
    rows = []
    def add(areset=0, bump_left=0, bump_right=0, ground=1, dig=0, mid=None):
        r = {'areset': areset, 'bump_left': bump_left, 'bump_right': bump_right, 'ground': ground, 'dig': dig}
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
    add(dig=1, ground=0)
    add(ground=0)
    add(ground=1)
    add(ground=0, mid={'ground': 1})
    add(ground=0)
    for _ in range(25):
        add(ground=0)
    add(ground=1)
    add(areset=1, bump_left=1)
    add()
    while len(rows) < cycles:
        add(
            areset=1 if rng.random() < 0.02 else 0,
            bump_left=rng.getrandbits(1),
            bump_right=rng.getrandbits(1),
            ground=rng.getrandbits(1),
            dig=rng.getrandbits(1),
            mid={'ground': rng.getrandbits(1)} if rng.random() < 0.1 else None
        )
    return rows[:cycles]

def stimulus(rng, cycles):
    rows = []
    def add(x, y, mid=None):
        d = {'x': x & 1, 'y': y & 7}
        if mid is not None:
            d['mid'] = {k: v & (1 if k == 'x' else 7) for k, v in mid.items()}
        rows.append(d)
    add(0, 0); add(1, 0); add(0, 1); add(1, 1)
    add(0, 2); add(1, 2); add(0, 3); add(1, 3)
    add(0, 4); add(1, 4); add(0, 5); add(1, 5)
    add(0, 6); add(1, 6); add(0, 7); add(1, 7)
    while len(rows) < cycles:
        x = rng.getrandbits(1)
        y = rng.randrange(8)
        if rng.random() < 0.5:
            mid = {'x': rng.getrandbits(1)}
            if rng.random() < 0.5:
                mid['y'] = rng.randrange(8)
            add(x, y, mid)
        else:
            add(x, y)
    return rows[:cycles]

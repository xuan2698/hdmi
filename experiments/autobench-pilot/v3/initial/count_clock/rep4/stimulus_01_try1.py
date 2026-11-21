def stimulus(rng, cycles):
    rows = []
    def row(reset=0, ena=0, mid=None):
        d = {'reset': reset, 'ena': ena}
        if mid is not None:
            d['mid'] = mid
        rows.append(d)
    row(1, 0)
    row(1, 1)
    row(0, 0)
    row(0, 1)
    for _ in range(4):
        row(0, 1)
    row(0, 0)
    row(0, 1, {'ena': 0})
    row(0, 1, {'reset': 1})
    row(0, 0, {'ena': 1})
    row(1, 1, {'reset': 0})
    row(0, 1)
    while len(rows) < cycles:
        r = rng.randrange(100)
        if r < 5:
            row(1, rng.getrandbits(1))
        elif r < 15:
            row(0, 0)
        elif r < 25:
            row(0, 1, {'ena': 0} if rng.getrandbits(1) else {'reset': 1})
        elif r < 35:
            row(0, 0, {'ena': 1})
        else:
            row(0, 1)
    return rows[:cycles]

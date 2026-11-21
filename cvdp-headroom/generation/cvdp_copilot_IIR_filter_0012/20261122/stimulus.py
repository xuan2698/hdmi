def stimulus(rng, cycles):
    rows = []
    def add(r, a, b, c, f, mid=None):
        row = {'reset': r, 'in_1': a & 0xFFFF, 'in_2': b & 0xFFFF,
               'in_3': c & 0xFFFF, 'filter_select': f & 3}
        if mid:
            row['mid'] = mid
        rows.append(row)

    # Reset phase
    for _ in range(3):
        add(1, 0, 0, 0, 0)
    add(0, 0, 0, 0, 0)

    # Edge cases
    edges = [(0x7FFF, 0x8000, 0x7FFF, 0), (0x8000, 0x7FFF, 0x7FFF, 1),
             (0xAAAA, 0x5555, 0xAAAA, 2), (0, 0, 0, 3),
             (0x1234, 0x5678, 0x9ABC, 0), (0xFFFF, 0xFFFF, 0xFFFF, 1),
             (0x7FFF, 0x7FFF, 0x7FFF, 2), (0x8000, 0x8000, 0x8000, 3)]
    for e in edges:
        for _ in range(3):
            add(0, *e)

    # Step test
    for _ in range(20):
        add(0, 0x1000, 0x1000, 0x1000, 0)
    for _ in range(20):
        add(0, 0, 0, 0, 0)

    # Single channel tests
    for ch in range(3):
        for f in range(4):
            for _ in range(4):
                a = 0x2000 if ch == 0 else 0
                b = 0x2000 if ch == 1 else 0
                c = 0x2000 if ch == 2 else 0
                add(0, a, b, c, f)

    # Coefficient transition
    for f in range(4):
        for _ in range(6):
            add(0, 0x0800, 0x0800, 0x0800, f)

    # Dynamic switching every 10 cycles
    for blk in range(6):
        f = blk % 4
        for _ in range(10):
            add(0, rng.randrange(0x10000), rng.randrange(0x10000),
                rng.randrange(0x10000), f)

    # Mid-cycle changes
    for _ in range(10):
        add(0, rng.randrange(0x10000), rng.randrange(0x10000),
            rng.randrange(0x10000), rng.randrange(4),
            mid={'in_1': rng.randrange(0x10000), 'filter_select': rng.randrange(4)})

    # Random stress fill
    while len(rows) < cycles:
        add(0, rng.randrange(0x10000), rng.randrange(0x10000),
            rng.randrange(0x10000), rng.randrange(4))

    return rows[:cycles]

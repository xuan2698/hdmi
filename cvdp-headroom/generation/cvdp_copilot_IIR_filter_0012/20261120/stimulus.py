def stimulus(rng, cycles):
    rows = []
    def row(reset, a, b, c, sel, mid=None):
        d = {'reset': reset, 'in_1': a & 0xFFFF, 'in_2': b & 0xFFFF,
             'in_3': c & 0xFFFF, 'filter_select': sel & 3}
        if mid is not None:
            d['mid'] = mid
        rows.append(d)

    # Reset phase
    for _ in range(3):
        row(1, 0, 0, 0, 0)
    row(0, 0, 0, 0, 0)

    # Edge cases
    edges = [(0x7FFF, 0x8000, 0x7FFF, 0), (0x8000, 0x7FFF, 0x7FFF, 1),
             (0xAAAA, 0x5555, 0xAAAA, 2), (0, 0, 0, 3),
             (0x1234, 0x5678, 0x9ABC, 0), (0xFFFF, 0xFFFF, 0xFFFF, 1),
             (0x8000, 0x8000, 0x8000, 2), (0x7FFF, 0x7FFF, 0x7FFF, 3)]
    for e in edges:
        for _ in range(3):
            row(0, e[0], e[1], e[2], e[3])

    # Step test
    for _ in range(20):
        row(0, 0x1000, 0x1000, 0x1000, 0)
    for _ in range(20):
        row(0, 0, 0, 0, 0)

    # Single channel tests
    for ch in range(3):
        for sel in range(4):
            for _ in range(4):
                a = 0x2000 if ch == 0 else 0
                b = 0x2000 if ch == 1 else 0
                c = 0x2000 if ch == 2 else 0
                row(0, a, b, c, sel)

    # Coefficient transition: constant input, cycle selects
    for _ in range(8):
        for sel in range(4):
            row(0, 0x0800, 0x0800, 0x0800, sel)

    # Dynamic switching every 10 cycles
    for blk in range(6):
        sel = rng.randrange(4)
        for _ in range(10):
            row(0, rng.randrange(0x10000), rng.randrange(0x10000),
                rng.randrange(0x10000), sel)

    # Mid-cycle changes
    for _ in range(10):
        row(0, rng.randrange(0x10000), rng.randrange(0x10000),
            rng.randrange(0x10000), rng.randrange(4),
            mid={'in_1': rng.randrange(0x10000), 'filter_select': rng.randrange(4)})

    # Post-reset behavior
    row(1, 0, 0, 0, 0)
    row(1, 0x7FFF, 0x7FFF, 0x7FFF, 1)
    row(0, 0x7FFF, 0x7FFF, 0x7FFF, 1)
    for _ in range(10):
        row(0, 0x7FFF, 0x7FFF, 0x7FFF, 1)

    # Random stress fill
    while len(rows) < cycles:
        row(0, rng.randrange(0x10000), rng.randrange(0x10000),
            rng.randrange(0x10000), rng.randrange(4))

    return rows[:cycles]

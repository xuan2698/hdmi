def stimulus(rng, cycles):
    rows = []
    def add(rst, a, b, c, sel, mid=None):
        row = {'reset': rst, 'in_1': a & 0xFFFF, 'in_2': b & 0xFFFF,
               'in_3': c & 0xFFFF, 'filter_select': sel & 3}
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
             (0x8000, 0x8000, 0x8000, 2), (0x7FFF, 0x7FFF, 0x7FFF, 3)]
    for e in edges:
        add(0, *e)
        add(0, *e)

    # Step test
    for _ in range(8):
        add(0, 0x1000, 0x1000, 0x1000, 0)
    for _ in range(8):
        add(0, 0, 0, 0, 0)

    # Single channel tests
    for ch in range(3):
        for sel in range(4):
            vals = [0, 0, 0]
            vals[ch] = 0x2000
            for _ in range(4):
                add(0, vals[0], vals[1], vals[2], sel)

    # Coefficient transition: constant input, cycle select
    for sel in [0, 1, 2, 3, 0, 2, 1, 3, 0, 1, 2, 3]:
        for _ in range(3):
            add(0, 0x0800, 0x0800, 0x0800, sel)

    # All-zero across selects
    for sel in range(4):
        for _ in range(3):
            add(0, 0, 0, 0, sel)

    # Post-reset behavior
    add(1, 0x7FFF, 0x7FFF, 0x7FFF, 0)
    add(1, 0, 0, 0, 0)
    add(0, 0x1000, 0x2000, 0x3000, 1)
    add(0, 0x1000, 0x2000, 0x3000, 1)

    # Overflow / saturation stress
    for _ in range(10):
        add(0, 0x7FFF, 0x8000, 0x7FFF, rng.randrange(4))
        add(0, 0x8000, 0x7FFF, 0x8000, rng.randrange(4))

    # Dynamic switching every 10 cycles with random data
    sel = rng.randrange(4)
    for i in range(60):
        if i % 10 == 0:
            sel = rng.randrange(4)
        add(0, rng.randrange(0x10000), rng.randrange(0x10000),
            rng.randrange(0x10000), sel)

    # Mid-cycle changes on some rows
    for _ in range(20):
        a = rng.randrange(0x10000)
        b = rng.randrange(0x10000)
        c = rng.randrange(0x10000)
        s = rng.randrange(4)
        mid = {'in_1': rng.randrange(0x10000),
               'filter_select': rng.randrange(4)}
        add(0, a, b, c, s, mid)

    # Fill remaining with random exploration
    while len(rows) < cycles:
        r = rng.random()
        if r < 0.05:
            add(1, rng.randrange(0x10000), rng.randrange(0x10000),
                rng.randrange(0x10000), rng.randrange(4))
        elif r < 0.15:
            add(0, 0x7FFF, 0x8000, 0x7FFF, rng.randrange(4))
        elif r < 0.25:
            add(0, 0, 0, 0, rng.randrange(4))
        else:
            add(0, rng.randrange(0x10000), rng.randrange(0x10000),
                rng.randrange(0x10000), rng.randrange(4))

    return rows[:cycles]

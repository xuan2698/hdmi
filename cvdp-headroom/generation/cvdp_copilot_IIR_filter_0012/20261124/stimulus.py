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
    edges = [(0x7FFF, 0x8000, 0x7FFF), (0x8000, 0x7FFF, 0x8000),
             (0xAAAA, 0x5555, 0xAAAA), (0x5555, 0xAAAA, 0x5555),
             (0x0000, 0x0000, 0x0000), (0xFFFF, 0xFFFF, 0xFFFF),
             (0x1234, 0x5678, 0x9ABC), (0x7FFF, 0x7FFF, 0x7FFF),
             (0x8000, 0x8000, 0x8000)]
    for i, (a, b, c) in enumerate(edges):
        add(0, a, b, c, i % 4)
        add(0, a, b, c, i % 4)

    # Invalid filter_select sweep
    for f in range(4):
        for _ in range(4):
            add(0, 0x1000, 0x2000, 0x3000, f)

    # Step test
    for _ in range(8):
        add(0, 0x1000, 0x1000, 0x1000, 0)
    for _ in range(8):
        add(0, 0, 0, 0, 0)

    # Coefficient transition: constant input, cycle selects
    for k in range(12):
        add(0, 0x0800, 0x0800, 0x0800, k % 4)

    # Single channel tests
    for ch in range(3):
        for _ in range(6):
            a = 0x2000 if ch == 0 else 0
            b = 0x2000 if ch == 1 else 0
            c = 0x2000 if ch == 2 else 0
            add(0, a, b, c, ch)

    # All-zero across selects
    for f in range(4):
        for _ in range(3):
            add(0, 0, 0, 0, f)

    # Post-reset behavior
    add(1, 0, 0, 0, 0)
    add(1, 0, 0, 0, 0)
    add(0, 0x0FFF, 0x0FFF, 0x0FFF, 1)
    for _ in range(5):
        add(0, 0x0FFF, 0x0FFF, 0x0FFF, 1)

    # Overflow / saturation
    for _ in range(6):
        add(0, 0x7FFF, 0x8000, 0x7FFF, 2)
        add(0, 0x8000, 0x7FFF, 0x8000, 3)

    # Dynamic switching every 10 cycles
    while len(rows) < cycles - 400:
        f = rng.randrange(4)
        for _ in range(10):
            if len(rows) >= cycles - 400:
                break
            add(0, rng.randrange(1 << 16), rng.randrange(1 << 16),
                rng.randrange(1 << 16), f)

    # Mid-cycle changes on some rows
    for _ in range(20):
        if len(rows) >= cycles - 300:
            break
        add(0, rng.randrange(1 << 16), rng.randrange(1 << 16),
            rng.randrange(1 << 16), rng.randrange(4),
            mid={'in_1': rng.randrange(1 << 16),
                 'filter_select': rng.randrange(4)})

    # Random stress fill
    while len(rows) < cycles:
        add(0, rng.randrange(1 << 16), rng.randrange(1 << 16),
            rng.randrange(1 << 16), rng.randrange(4))

    return rows[:cycles]

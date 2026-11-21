def stimulus(rng, cycles):
    rows = []
    # Directed edge cases
    directed = [
        (0, 0),
        (0, (1 << 45) - 1),
        ((1 << 15) - 1, 0),
        ((1 << 15) - 1, (1 << 45) - 1),
        (0x7FFF, 0x1FFFFFFFFFFFF),
        (0x0001, 0x0000000000001),
        (0x7C00, 0x1F7C000000000),
        (0x03FF, 0x00000000003FF),
        (0x4210, 0x10842108421),
        (0x7FFF, 0x0000000000000),
        (0x0000, 0x1FFFFFFFFFFFF),
        (0x5294, 0x0A5294A5294),
        (0x6B5A, 0x1B5AD6B5AD6),
        (0x7FFF, 0x1FFFFFFFFFFFF),
        (0x0000, 0x0000000000000),
    ]
    # Build a sequence: reset pulse, then directed tests with start strobes
    idx = 0
    # Initial reset for a few cycles
    for _ in range(3):
        rows.append({'reset': 1, 'start': 0, 'plaintext': 0, 'key': 0})
        idx += 1
    # Directed tests: each test holds inputs, pulses start for 1 cycle, then waits
    di = 0
    while idx < cycles:
        if di < len(directed):
            pt, ky = directed[di]
            di += 1
        else:
            # Random exploration
            pt = rng.randrange(1 << 15)
            ky = rng.randrange(1 << 45)
        # Hold inputs for a few cycles with start=0, then pulse start
        hold = rng.randrange(1, 4)
        for h in range(hold):
            if idx >= cycles:
                break
            rows.append({'reset': 0, 'start': 0, 'plaintext': pt, 'key': ky})
            idx += 1
        if idx >= cycles:
            break
        # Start pulse cycle
        rows.append({'reset': 0, 'start': 1, 'plaintext': pt, 'key': ky})
        idx += 1
        # Wait cycles for done (FSM takes ~3-4 cycles)
        wait = rng.randrange(3, 6)
        for w in range(wait):
            if idx >= cycles:
                break
            rows.append({'reset': 0, 'start': 0, 'plaintext': pt, 'key': ky})
            idx += 1
        # Occasionally inject a reset
        if rng.random() < 0.08 and idx < cycles:
            rows.append({'reset': 1, 'start': 0, 'plaintext': 0, 'key': 0})
            idx += 1
            rows.append({'reset': 0, 'start': 0, 'plaintext': 0, 'key': 0})
            idx += 1
    # Trim or pad to exactly cycles
    while len(rows) < cycles:
        rows.append({'reset': 0, 'start': 0, 'plaintext': 0, 'key': 0})
    return rows[:cycles]

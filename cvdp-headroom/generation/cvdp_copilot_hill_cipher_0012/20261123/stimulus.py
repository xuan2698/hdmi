def stimulus(rng, cycles):
    rows = []
    # Directed edge cases
    edges = [
        (0, 0),
        (0, (1 << 45) - 1),
        ((1 << 15) - 1, 0),
        ((1 << 15) - 1, (1 << 45) - 1),
        (0x7FFF, 0x1FFFFFFFFFF),
        (0x0001, 0x00000000001),
        (0x7C00, 0x1F7DF7DF7DF),
        (0x03FF, 0x000000003FF),
        (0x4210, 0x10842108421),
        (0x7FFF, 0x00000000000),
    ]
    # Build a sequence: reset pulse, then directed cases with start strobes,
    # then random exploration.
    idx = 0
    # Initial reset for a few cycles
    for _ in range(3):
        rows.append({'reset': 1, 'start': 0, 'plaintext': 0, 'key': 0})
    # Directed cases: set inputs, pulse start, wait for done (4 cycles total per request)
    for pt, k in edges:
        # cycle 1: set inputs, start=1
        rows.append({'reset': 0, 'start': 1, 'plaintext': pt, 'key': k})
        # cycles 2-4: start=0, wait for done
        for _ in range(3):
            rows.append({'reset': 0, 'start': 0, 'plaintext': pt, 'key': k})
    # Random exploration with occasional back-to-back starts and mid-cycle changes
    while len(rows) < cycles:
        r = rng.random()
        pt = rng.getrandbits(15)
        k = rng.getrandbits(45)
        if r < 0.15:
            # back-to-back start requests
            rows.append({'reset': 0, 'start': 1, 'plaintext': pt, 'key': k})
            rows.append({'reset': 0, 'start': 1, 'plaintext': rng.getrandbits(15), 'key': rng.getrandbits(45)})
            rows.append({'reset': 0, 'start': 0, 'plaintext': pt, 'key': k})
            rows.append({'reset': 0, 'start': 0, 'plaintext': pt, 'key': k})
        elif r < 0.25:
            # mid-cycle change on plaintext/key
            rows.append({'reset': 0, 'start': 1, 'plaintext': pt, 'key': k,
                         'mid': {'plaintext': rng.getrandbits(15), 'key': rng.getrandbits(45)}})
            rows.append({'reset': 0, 'start': 0, 'plaintext': pt, 'key': k})
            rows.append({'reset': 0, 'start': 0, 'plaintext': pt, 'key': k})
            rows.append({'reset': 0, 'start': 0, 'plaintext': pt, 'key': k})
        elif r < 0.30:
            # reset pulse in middle of operation
            rows.append({'reset': 0, 'start': 1, 'plaintext': pt, 'key': k})
            rows.append({'reset': 1, 'start': 0, 'plaintext': pt, 'key': k})
            rows.append({'reset': 0, 'start': 0, 'plaintext': pt, 'key': k})
            rows.append({'reset': 0, 'start': 0, 'plaintext': pt, 'key': k})
        else:
            # normal request
            rows.append({'reset': 0, 'start': 1, 'plaintext': pt, 'key': k})
            rows.append({'reset': 0, 'start': 0, 'plaintext': pt, 'key': k})
            rows.append({'reset': 0, 'start': 0, 'plaintext': pt, 'key': k})
            rows.append({'reset': 0, 'start': 0, 'plaintext': pt, 'key': k})
    return rows[:cycles]

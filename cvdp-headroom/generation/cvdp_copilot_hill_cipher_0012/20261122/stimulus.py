def stimulus(rng, cycles):
    rows = []
    # Directed edge cases
    directed = [
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
        (1, 0, 0),
        (0x7FFF, 0x7FFFFFFFFFF, 1),
        (0x7FFF, 0x7FFFFFFFFFF, 0),
        (0x0001, 0x00000000001, 1),
        (0x7C00, 0x7C000000000, 1),
        (0x001F, 0x0000000001F, 1),
        (0x4210, 0x10842108421, 1),
        (0x7FFF, 0x00000000000, 1),
        (0x0000, 0x7FFFFFFFFFF, 1),
    ]
    # Build a schedule: reset pulse, then directed, then random with start pulses
    idx = 0
    # Initial reset for a few cycles
    for _ in range(3):
        rows.append({'reset': 1, 'start': 0, 'plaintext': 0, 'key': 0})
    # Directed tests: set inputs, pulse start, wait for done (4 cycles total per test)
    for pt, ky, st in directed:
        # cycle 1: set inputs, start=1
        rows.append({'reset': 0, 'start': 1, 'plaintext': pt & 0x7FFF, 'key': ky & 0x7FFFFFFFFFF})
        # cycles 2-4: start=0, wait
        for _ in range(3):
            rows.append({'reset': 0, 'start': 0, 'plaintext': pt & 0x7FFF, 'key': ky & 0x7FFFFFFFFFF})
    # Fill remaining with random exploration
    while len(rows) < cycles:
        r = rng.random()
        if r < 0.05:
            # occasional reset
            rows.append({'reset': 1, 'start': 0, 'plaintext': 0, 'key': 0})
        elif r < 0.35:
            # start pulse with random data
            pt = rng.getrandbits(15)
            ky = rng.getrandbits(45)
            rows.append({'reset': 0, 'start': 1, 'plaintext': pt, 'key': ky})
        else:
            # idle with random data (start=0)
            pt = rng.getrandbits(15)
            ky = rng.getrandbits(45)
            rows.append({'reset': 0, 'start': 0, 'plaintext': pt, 'key': ky})
    return rows[:cycles]

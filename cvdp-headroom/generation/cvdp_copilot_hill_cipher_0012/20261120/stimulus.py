def stimulus(rng, cycles):
    rows = []
    # Directed edge cases
    edges = [
        (0, 0),
        (0x7FFF, 0x7FFFFFFFFFFF),
        (0x7FFF, 0),
        (0, 0x7FFFFFFFFFFF),
        (0x4210, 0x1084210842108421 & 0x7FFFFFFFFFFF),
        (0x7FFF, 0x7FFFFFFFFFFF),
        (0x0001, 0x0000000001),
        (0x7C00, 0x7C0000000000),
    ]
    # Build a schedule: mostly idle with periodic start pulses
    # We'll interleave: reset phase, then repeated (idle, start, idle, idle, idle) patterns
    idx = 0
    edge_idx = 0
    # Phase 1: reset for a few cycles
    for _ in range(3):
        rows.append({'reset': 1, 'start': 0, 'plaintext': 0, 'key': 0})
    # Phase 2: directed and random sequences
    while len(rows) < cycles:
        # Occasionally assert reset
        if rng.random() < 0.03:
            rows.append({'reset': 1, 'start': 0, 'plaintext': 0, 'key': 0})
            continue
        # Choose plaintext/key
        if edge_idx < len(edges) and rng.random() < 0.5:
            pt, k = edges[edge_idx]
            edge_idx += 1
        elif rng.random() < 0.3:
            # structured: small letters
            pt = rng.randrange(0, 1 << 15)
            k = rng.randrange(0, 1 << 45)
        else:
            pt = rng.randrange(0, 1 << 15)
            k = rng.randrange(0, 1 << 45)
        # Idle cycle before start
        rows.append({'reset': 0, 'start': 0, 'plaintext': pt, 'key': k})
        if len(rows) >= cycles:
            break
        # Start pulse
        rows.append({'reset': 0, 'start': 1, 'plaintext': pt, 'key': k})
        if len(rows) >= cycles:
            break
        # Wait cycles for done (3 cycles after start: COMPUTE, COMPUTE_MOD, DONE)
        # Add some idle cycles, sometimes back-to-back starts
        wait = rng.choice([2, 3, 3, 4, 5])
        for w in range(wait):
            if len(rows) >= cycles:
                break
            # Occasionally change plaintext/key mid-wait (shouldn't affect in-flight)
            if rng.random() < 0.2:
                pt2 = rng.randrange(0, 1 << 15)
                k2 = rng.randrange(0, 1 << 45)
                rows.append({'reset': 0, 'start': 0, 'plaintext': pt2, 'key': k2})
            else:
                rows.append({'reset': 0, 'start': 0, 'plaintext': pt, 'key': k})
        # Sometimes do back-to-back start
        if rng.random() < 0.25 and len(rows) < cycles:
            pt3 = rng.randrange(0, 1 << 15)
            k3 = rng.randrange(0, 1 << 45)
            rows.append({'reset': 0, 'start': 1, 'plaintext': pt3, 'key': k3})
    # Trim/pad to exactly cycles
    while len(rows) < cycles:
        rows.append({'reset': 0, 'start': 0, 'plaintext': 0, 'key': 0})
    return rows[:cycles]

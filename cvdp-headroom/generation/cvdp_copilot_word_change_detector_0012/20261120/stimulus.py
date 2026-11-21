def stimulus(rng, cycles):
    rows = []
    # Phase 1: reset for 3 cycles
    for _ in range(3):
        rows.append({'reset': 1, 'data_in': 0, 'mask': 0, 'match_pattern': 0,
                     'enable': 0, 'latch_pattern': 0})
    # Phase 2: latch zero pattern, then word change tests
    seq = [
        (0, 0xFF, 0x00, 1, 1),   # latch zero pattern
        (0x00, 0xFF, 0x00, 1, 0),
        (0xFF, 0xFF, 0x00, 1, 0),  # 0->1 all bits
        (0x00, 0xFF, 0x00, 1, 0),  # 1->0 all bits
        (0x01, 0xFF, 0x00, 1, 0),  # LSB flip
        (0x00, 0xFF, 0x00, 1, 0),
        (0x80, 0xFF, 0x00, 1, 0),  # MSB flip
        (0x00, 0xFF, 0x00, 1, 0),
        (0xAA, 0xFF, 0x00, 1, 0),  # alternating
        (0x55, 0xFF, 0x00, 1, 0),
        (0x55, 0xFF, 0x00, 1, 0),  # no change
        (0x55, 0xFF, 0x00, 1, 0),
    ]
    for d, m, p, e, l in seq:
        rows.append({'reset': 0, 'data_in': d, 'mask': m, 'match_pattern': p,
                     'enable': e, 'latch_pattern': l})
    # Phase 3: pattern match tests
    seq = [
        (0x00, 0xFF, 0xA5, 1, 1),  # latch A5
        (0xA5, 0xFF, 0xA5, 1, 0),  # match full mask
        (0x5A, 0xFF, 0xA5, 1, 0),  # mismatch
        (0xA5, 0x0F, 0xA5, 1, 0),  # partial mask match
        (0xAF, 0x0F, 0xA5, 1, 0),  # partial mask match (upper ignored)
        (0xA5, 0xF0, 0xA5, 1, 0),  # partial mask mismatch
    ]
    for d, m, p, e, l in seq:
        rows.append({'reset': 0, 'data_in': d, 'mask': m, 'match_pattern': p,
                     'enable': e, 'latch_pattern': l})
    # Phase 4: masking behavior
    seq = [
        (0x00, 0xFF, 0x00, 1, 0),
        (0xFF, 0xFF, 0x00, 1, 0),  # full mask change
        (0x00, 0x00, 0x00, 1, 0),  # no mask
        (0xFF, 0x00, 0x00, 1, 0),  # no mask change suppressed
        (0x0F, 0x0F, 0x00, 1, 0),
        (0xF0, 0x0F, 0x00, 1, 0),  # masked change
        (0xAA, 0xAA, 0x00, 1, 0),
        (0x55, 0xAA, 0x00, 1, 0),
    ]
    for d, m, p, e, l in seq:
        rows.append({'reset': 0, 'data_in': d, 'mask': m, 'match_pattern': p,
                     'enable': e, 'latch_pattern': l})
    # Phase 5: enable control
    seq = [
        (0x00, 0xFF, 0x00, 0, 0),
        (0xFF, 0xFF, 0x00, 0, 0),  # disabled, no pulse
        (0x00, 0xFF, 0x00, 0, 0),
        (0xFF, 0xFF, 0x00, 1, 0),  # re-enable
        (0x00, 0xFF, 0x00, 1, 0),
    ]
    for d, m, p, e, l in seq:
        rows.append({'reset': 0, 'data_in': d, 'mask': m, 'match_pattern': p,
                     'enable': e, 'latch_pattern': l})
    # Phase 6: combined change + match with masking
    seq = [
        (0x00, 0xFF, 0x3C, 1, 1),  # latch 3C
        (0x3C, 0xFF, 0x3C, 1, 0),  # match, change
        (0x3C, 0xFF, 0x3C, 1, 0),  # no change, match
        (0x3D, 0xFF, 0x3C, 1, 0),  # single bit change
        (0x3C, 0xFF, 0x3C, 1, 0),
        (0xFC, 0x0F, 0x3C, 1, 0),  # upper bits change, masked
        (0x3C, 0x0F, 0x3C, 1, 0),
        (0x00, 0xFF, 0x3C, 1, 0),  # multiple bit change
        (0x3C, 0xFF, 0x3C, 1, 0),
    ]
    for d, m, p, e, l in seq:
        rows.append({'reset': 0, 'data_in': d, 'mask': m, 'match_pattern': p,
                     'enable': e, 'latch_pattern': l})
    # Phase 7: stress random
    while len(rows) < cycles:
        r = rng.random()
        if r < 0.05:
            rows.append({'reset': 1, 'data_in': 0, 'mask': 0, 'match_pattern': 0,
                         'enable': 0, 'latch_pattern': 0})
        else:
            d = rng.randrange(256)
            m = rng.choice([0x00, 0xFF, 0x0F, 0xF0, 0xAA, 0x55, rng.randrange(256)])
            p = rng.randrange(256)
            e = 1 if rng.random() < 0.85 else 0
            l = 1 if rng.random() < 0.1 else 0
            row = {'reset': 0, 'data_in': d, 'mask': m, 'match_pattern': p,
                   'enable': e, 'latch_pattern': l}
            if rng.random() < 0.15:
                row['mid'] = {'data_in': rng.randrange(256),
                              'mask': rng.choice([0x00, 0xFF, rng.randrange(256)])}
            rows.append(row)
    return rows[:cycles]

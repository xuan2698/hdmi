def stimulus(rng, cycles):
    rows = []
    # Phase 1: reset for 3 cycles
    for _ in range(3):
        rows.append({'reset': 1, 'data_in': 0, 'mask': 0, 'match_pattern': 0,
                     'enable': 0, 'latch_pattern': 0})
    # Phase 2: latch zero pattern, then word change tests
    seq = [
        (0x00, 0xFF, 0x00, 1, 1),
        (0xFF, 0xFF, 0x00, 1, 0),
        (0x00, 0xFF, 0x00, 1, 0),
        (0x01, 0xFF, 0x00, 1, 0),
        (0x00, 0xFF, 0x00, 1, 0),
        (0x80, 0xFF, 0x00, 1, 0),
        (0x00, 0xFF, 0x00, 1, 0),
        (0xAA, 0xFF, 0x00, 1, 0),
        (0x55, 0xFF, 0x00, 1, 0),
        (0x55, 0xFF, 0x00, 1, 0),
        (0x55, 0xFF, 0x00, 1, 0),
    ]
    for d, m, p, e, l in seq:
        rows.append({'reset': 0, 'data_in': d, 'mask': m, 'match_pattern': p,
                     'enable': e, 'latch_pattern': l})
    # Phase 3: pattern match tests
    seq = [
        (0xA5, 0xFF, 0xA5, 1, 1),
        (0xA5, 0xFF, 0xA5, 1, 0),
        (0x5A, 0xFF, 0xA5, 1, 0),
        (0xA5, 0xFF, 0xA5, 1, 0),
        (0xA0, 0xF0, 0xA5, 1, 0),
        (0xA5, 0xF0, 0xA5, 1, 0),
        (0xAF, 0xF0, 0xA5, 1, 0),
    ]
    for d, m, p, e, l in seq:
        rows.append({'reset': 0, 'data_in': d, 'mask': m, 'match_pattern': p,
                     'enable': e, 'latch_pattern': l})
    # Phase 4: masking behavior
    seq = [
        (0x00, 0xFF, 0x00, 1, 0),
        (0xFF, 0xFF, 0x00, 1, 0),
        (0xFF, 0x00, 0x00, 1, 0),
        (0x00, 0x00, 0x00, 1, 0),
        (0x3C, 0x0F, 0x00, 1, 0),
        (0xC3, 0x0F, 0x00, 1, 0),
        (0x3C, 0xF0, 0x00, 1, 0),
        (0x3C, 0xAA, 0x00, 1, 0),
        (0x3C, 0x55, 0x00, 1, 0),
    ]
    for d, m, p, e, l in seq:
        rows.append({'reset': 0, 'data_in': d, 'mask': m, 'match_pattern': p,
                     'enable': e, 'latch_pattern': l})
    # Phase 5: enable control
    seq = [
        (0x00, 0xFF, 0x00, 0, 0),
        (0xFF, 0xFF, 0x00, 0, 0),
        (0x00, 0xFF, 0x00, 0, 0),
        (0xAA, 0xFF, 0x00, 0, 0),
        (0x55, 0xFF, 0x00, 0, 0),
        (0x00, 0xFF, 0x00, 1, 0),
        (0xFF, 0xFF, 0x00, 1, 0),
    ]
    for d, m, p, e, l in seq:
        rows.append({'reset': 0, 'data_in': d, 'mask': m, 'match_pattern': p,
                     'enable': e, 'latch_pattern': l})
    # Phase 6: combined word change + pattern match with masking
    seq = [
        (0x00, 0xFF, 0x00, 1, 1),
        (0x00, 0xFF, 0x00, 1, 0),
        (0x01, 0xFF, 0x00, 1, 0),
        (0x03, 0xFF, 0x00, 1, 0),
        (0x07, 0xFF, 0x00, 1, 0),
        (0x0F, 0xFF, 0x00, 1, 0),
        (0x0F, 0x00, 0x00, 1, 0),
        (0xF0, 0x00, 0x00, 1, 0),
        (0xF0, 0x0F, 0x00, 1, 0),
        (0x00, 0x0F, 0x00, 1, 0),
        (0x00, 0xFF, 0x00, 1, 0),
        (0x00, 0xFF, 0x00, 1, 0),
        (0x00, 0xFF, 0x00, 1, 0),
        (0x0F, 0xFF, 0x00, 1, 0),
        (0x0F, 0xFF, 0x00, 1, 0),
        (0xF0, 0xFF, 0x00, 1, 0),
        (0xF0, 0xFF, 0x00, 1, 0),
    ]
    for d, m, p, e, l in seq:
        rows.append({'reset': 0, 'data_in': d, 'mask': m, 'match_pattern': p,
                     'enable': e, 'latch_pattern': l})
    # Phase 7: stress with random data, occasional latch/enable toggles
    prev = 0x00
    for i in range(cycles - len(rows)):
        r = rng.random()
        if r < 0.05:
            d = rng.randrange(256)
            m = rng.randrange(256)
            p = rng.randrange(256)
            e = rng.randrange(2)
            l = rng.randrange(2)
        elif r < 0.15:
            d = prev ^ (1 << rng.randrange(8))
            m = rng.choice([0x00, 0xFF, 0x0F, 0xF0, rng.randrange(256)])
            p = rng.randrange(256)
            e = 1
            l = 0
        else:
            d = rng.randrange(256)
            m = rng.choice([0x00, 0xFF, 0x0F, 0xF0, 0xAA, 0x55, rng.randrange(256)])
            p = rng.randrange(256)
            e = 1 if rng.random() < 0.9 else 0
            l = 1 if rng.random() < 0.05 else 0
        prev = d
        row = {'reset': 0, 'data_in': d, 'mask': m, 'match_pattern': p,
               'enable': e, 'latch_pattern': l}
        if rng.random() < 0.1:
            row['mid'] = {'data_in': rng.randrange(256)}
        rows.append(row)
    return rows[:cycles]

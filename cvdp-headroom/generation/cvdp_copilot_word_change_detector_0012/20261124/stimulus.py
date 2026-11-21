def stimulus(rng, cycles):
    rows = []
    # initial state
    data = 0
    mask = 0xFF
    pat = 0
    en = 1
    lp = 0

    def emit(d, m, p, e, l, mid=None):
        r = {'reset': 0, 'data_in': d & 0xFF, 'mask': m & 0xFF,
             'match_pattern': p & 0xFF, 'enable': e & 1, 'latch_pattern': l & 1}
        if mid:
            r['mid'] = mid
        rows.append(r)

    # Phase 0: reset for 3 cycles
    for _ in range(3):
        rows.append({'reset': 1, 'data_in': 0, 'mask': 0xFF,
                     'match_pattern': 0, 'enable': 0, 'latch_pattern': 0})

    # Phase 1: latch zero pattern
    emit(0, 0xFF, 0, 1, 1)
    emit(0, 0xFF, 0, 1, 0)

    # Phase 2: word change tests
    seq = [0xFF, 0x00, 0x01, 0x80, 0xAA, 0x55, 0xAA, 0x55, 0x55, 0x55]
    for v in seq:
        emit(v, 0xFF, 0, 1, 0)

    # Phase 3: pattern match tests
    emit(0x00, 0xFF, 0xA5, 1, 1)  # latch A5
    emit(0x00, 0xFF, 0xA5, 1, 0)
    for v in [0xA5, 0x5A, 0xA5, 0x00, 0xFF, 0xA5]:
        emit(v, 0xFF, 0xA5, 1, 0)
    # partial mask
    for v in [0xA5, 0xAF, 0x5A, 0xA0]:
        emit(v, 0xF0, 0xA5, 1, 0)

    # Phase 4: masking behavior
    emit(0x00, 0xFF, 0x00, 1, 1)
    emit(0x00, 0xFF, 0x00, 1, 0)
    for v in [0xFF, 0x00, 0xFF, 0x00]:
        emit(v, 0xFF, 0x00, 1, 0)
    for v in [0xFF, 0x00, 0xFF, 0x00]:
        emit(v, 0x00, 0x00, 1, 0)
    for m in [0x0F, 0xF0, 0xAA, 0x55, 0x81, 0x18]:
        emit(0x00, m, 0x00, 1, 0)
        emit(0xFF, m, 0x00, 1, 0)
        emit(0x00, m, 0x00, 1, 0)

    # Phase 5: enable control
    emit(0x00, 0xFF, 0x00, 1, 1)
    emit(0x00, 0xFF, 0x00, 1, 0)
    for v in [0xFF, 0x00, 0xFF, 0xAA, 0x55]:
        emit(v, 0xFF, 0x00, 0, 0)
    emit(0x00, 0xFF, 0x00, 1, 0)
    emit(0xFF, 0xFF, 0x00, 1, 0)

    # Phase 6: combined word change + pattern match with masking
    emit(0x00, 0xFF, 0x3C, 1, 1)
    emit(0x00, 0xFF, 0x3C, 1, 0)
    for v in [0x3C, 0x3C, 0x3D, 0x3C, 0x00, 0x3C, 0xFF, 0x3C]:
        emit(v, 0xFF, 0x3C, 1, 0)
    # partial mask upper bits transition
    for v in [0x00, 0xF0, 0x0F, 0xF0, 0x00]:
        emit(v, 0x0F, 0x00, 1, 0)

    # Phase 7: stress random
    while len(rows) < cycles - 5:
        d = rng.randrange(256)
        m = rng.choice([0x00, 0xFF, 0x0F, 0xF0, rng.randrange(256)])
        p = rng.randrange(256)
        e = 1 if rng.random() < 0.85 else 0
        l = 1 if rng.random() < 0.1 else 0
        mid = None
        if rng.random() < 0.15:
            mid = {'data_in': rng.randrange(256)}
        emit(d, m, p, e, l, mid)

    # pad to exact cycles
    while len(rows) < cycles:
        emit(0, 0xFF, 0, 1, 0)
    return rows[:cycles]

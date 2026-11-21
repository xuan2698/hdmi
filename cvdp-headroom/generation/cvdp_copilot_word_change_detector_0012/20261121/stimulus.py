def stimulus(rng, cycles):
    rows = []
    # state
    data = 0
    mask = 0xFF
    pat = 0
    en = 1
    lp = 0
    rst = 1

    def emit(rst, data, mask, pat, en, lp, mid=None):
        row = {'reset': rst, 'data_in': data & 0xFF, 'mask': mask & 0xFF,
               'match_pattern': pat & 0xFF, 'enable': en & 1, 'latch_pattern': lp & 1}
        if mid:
            row['mid'] = mid
        rows.append(row)

    # Phase: reset for 3 cycles
    for i in range(3):
        emit(1, 0, 0xFF, 0, 0, 0)
    rst = 0

    # Phase 1: latch zero pattern
    emit(0, 0, 0xFF, 0, 1, 1)
    emit(0, 0, 0xFF, 0, 1, 0)

    # Phase 2: word change tests
    seq = [0xFF, 0x00, 0x01, 0x80, 0xAA, 0x55, 0xAA, 0x55, 0x00, 0x00, 0xFF, 0x00]
    for v in seq:
        emit(0, v, 0xFF, 0, 1, 0)

    # Phase 3: pattern match tests
    emit(0, 0x5A, 0xFF, 0x5A, 1, 1)
    emit(0, 0x5A, 0xFF, 0x5A, 1, 0)
    emit(0, 0x5A, 0xFF, 0x5A, 1, 0)
    emit(0, 0xA5, 0xFF, 0x5A, 1, 0)
    emit(0, 0x5A, 0x0F, 0x5A, 1, 0)
    emit(0, 0x5B, 0x0F, 0x5A, 1, 0)
    emit(0, 0x5A, 0xF0, 0x5A, 1, 0)

    # Phase 4: masking behavior
    for m in [0xFF, 0x00, 0x0F, 0xF0, 0xAA, 0x55, 0x81, 0x7E]:
        emit(0, 0x3C, m, 0x3C, 1, 0)
        emit(0, 0xC3, m, 0x3C, 1, 0)
        emit(0, 0x3C, m, 0x3C, 1, 0)

    # Phase 5: enable control
    emit(0, 0xFF, 0xFF, 0x00, 0, 0)
    emit(0, 0x00, 0xFF, 0x00, 0, 0)
    emit(0, 0xAA, 0xFF, 0xAA, 0, 1)
    emit(0, 0xAA, 0xFF, 0xAA, 1, 0)
    emit(0, 0xAA, 0xFF, 0xAA, 1, 0)

    # Phase 6: combined scenarios
    emit(0, 0x00, 0xFF, 0x00, 1, 1)
    emit(0, 0x00, 0xFF, 0x00, 1, 0)
    emit(0, 0x00, 0xFF, 0x00, 1, 0)  # no change
    emit(0, 0x01, 0xFF, 0x00, 1, 0)  # single bit
    emit(0, 0x81, 0xFF, 0x00, 1, 0)  # multi bit
    emit(0, 0xFF, 0x00, 0x00, 1, 0)  # fully masked
    emit(0, 0x00, 0xFF, 0x00, 1, 0)
    emit(0, 0x00, 0xFF, 0x00, 1, 0)  # match no change
    emit(0, 0x0F, 0x0F, 0x00, 1, 0)
    emit(0, 0xF0, 0x0F, 0x00, 1, 0)

    # Phase 7: stress random
    while len(rows) < cycles - 4:
        r = rng.random()
        if r < 0.05:
            rst = 1
        else:
            rst = 0
        data = rng.randrange(256)
        mask = rng.choice([0x00, 0xFF, 0x0F, 0xF0, rng.randrange(256)])
        pat = rng.randrange(256)
        en = 1 if rng.random() < 0.85 else 0
        lp = 1 if rng.random() < 0.1 else 0
        mid = None
        if rng.random() < 0.15:
            mid = {'data_in': rng.randrange(256)}
        emit(rst, data, mask, pat, en, lp, mid)

    # pad
    while len(rows) < cycles:
        emit(0, 0, 0xFF, 0, 1, 0)

    return rows[:cycles]

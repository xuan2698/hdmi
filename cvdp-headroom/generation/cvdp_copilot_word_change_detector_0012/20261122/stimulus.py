def stimulus(rng, cycles):
    rows = []
    state = {
        'reset': 1, 'data_in': 0, 'mask': 0, 'match_pattern': 0,
        'enable': 0, 'latch_pattern': 0
    }
    def emit(mid=None):
        r = dict(state)
        if mid:
            r['mid'] = dict(mid)
        rows.append(r)
    # Reset phase: 3 cycles
    for _ in range(3):
        emit()
    state['reset'] = 0
    state['enable'] = 1
    state['mask'] = 0xFF
    # Phase 1: latch zero pattern
    state['latch_pattern'] = 1
    state['match_pattern'] = 0
    emit()
    state['latch_pattern'] = 0
    # Phase 2: word change tests
    seq = [0xFF, 0x00, 0x01, 0x00, 0x80, 0x00, 0xAA, 0x55, 0xAA, 0x55, 0x55]
    for v in seq:
        state['data_in'] = v
        emit()
    # Phase 3: pattern match tests
    state['latch_pattern'] = 1
    state['match_pattern'] = 0xA5
    emit()
    state['latch_pattern'] = 0
    for v in [0xA5, 0x5A, 0xA5, 0xA0, 0xA5, 0x0F]:
        state['data_in'] = v
        emit()
    # Phase 4: masking behavior
    state['mask'] = 0x00
    for v in [0x00, 0xFF, 0x55, 0xAA]:
        state['data_in'] = v
        emit()
    state['mask'] = 0xFF
    for m in [0x0F, 0xF0, 0x55, 0xAA, 0x33]:
        state['mask'] = m
        state['data_in'] = rng.randrange(256)
        emit()
    # Phase 5: enable control
    state['enable'] = 0
    for v in [0x00, 0xFF, 0x55, 0xAA]:
        state['data_in'] = v
        emit()
    state['enable'] = 1
    # Phase 6: combined scenarios
    state['mask'] = 0xFF
    state['latch_pattern'] = 1
    state['match_pattern'] = 0x3C
    emit()
    state['latch_pattern'] = 0
    state['data_in'] = 0x3C
    emit()
    state['data_in'] = 0x3D
    emit()
    state['data_in'] = 0x3C
    emit()
    state['mask'] = 0x0F
    state['data_in'] = 0x3F
    emit()
    state['data_in'] = 0x3C
    emit()
    state['mask'] = 0xF0
    state['data_in'] = 0xFC
    emit()
    state['data_in'] = 0x3C
    emit()
    # mid-cycle glitch
    state['data_in'] = 0x00
    emit({'data_in': 0xFF})
    state['data_in'] = 0xFF
    emit()
    # Phase 7: stress random
    while len(rows) < cycles - 5:
        state['data_in'] = rng.randrange(256)
        state['mask'] = rng.randrange(256)
        state['match_pattern'] = rng.randrange(256)
        state['enable'] = 1 if rng.random() < 0.85 else 0
        state['latch_pattern'] = 1 if rng.random() < 0.15 else 0
        if rng.random() < 0.2:
            mid = {'data_in': rng.randrange(256)}
            if rng.random() < 0.3:
                mid['mask'] = rng.randrange(256)
            emit(mid)
        else:
            emit()
    # tail: reset pulse
    state['reset'] = 1
    emit()
    state['reset'] = 0
    while len(rows) < cycles:
        emit()
    return rows[:cycles]

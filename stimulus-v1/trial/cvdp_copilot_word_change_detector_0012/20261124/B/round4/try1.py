def stimulus(rng, cycles):
    rows = []
    state = {
        'data_in': 0,
        'mask': 0,
        'match_pattern': 0,
        'enable': 0,
        'latch_pattern': 0,
    }
    reset_cycles = 4
    for i in range(cycles):
        row = {}
        if i < reset_cycles:
            row['reset'] = 1
            row['data_in'] = 0
            row['mask'] = 0
            row['match_pattern'] = 0
            row['enable'] = 0
            row['latch_pattern'] = 0
            rows.append(row)
            continue
        row['reset'] = 0
        phase = i % 48
        if phase < 5:
            state['enable'] = 1
            state['mask'] = 0xFF
            state['latch_pattern'] = 1 if phase == 0 else 0
            state['match_pattern'] = (state['data_in'] + 1) & 0xFF
            state['data_in'] = (state['data_in'] + 1) & 0xFF
        elif phase < 10:
            state['enable'] = 1
            state['mask'] = 0xFF
            state['latch_pattern'] = 0
            state['data_in'] = (state['data_in'] + 1) & 0xFF
        elif phase < 16:
            state['enable'] = 1
            state['mask'] = rng.choice([0x0F, 0xF0, 0xAA, 0x55, 0x00, 0xFF])
            state['latch_pattern'] = 0
            state['data_in'] = (state['data_in'] + rng.randrange(1, 4)) & 0xFF
        elif phase < 22:
            state['enable'] = 0
            state['latch_pattern'] = 0
            state['data_in'] = rng.randrange(0, 256)
        elif phase < 28:
            state['enable'] = 1
            state['mask'] = rng.randrange(0, 256)
            state['latch_pattern'] = 1 if rng.random() < 0.4 else 0
            state['match_pattern'] = rng.randrange(0, 256)
            state['data_in'] = rng.randrange(0, 256)
        elif phase < 34:
            state['enable'] = 1
            state['mask'] = 0xFF
            state['latch_pattern'] = 1
            state['match_pattern'] = state['data_in']
            state['data_in'] = (state['data_in'] + 1) & 0xFF
        else:
            state['enable'] = 1 if rng.random() < 0.85 else 0
            r = rng.random()
            if r < 0.4:
                state['mask'] = 0xFF
            elif r < 0.7:
                state['mask'] = rng.randrange(0, 256)
            else:
                state['mask'] = 0
            if rng.random() < 0.5:
                state['data_in'] = rng.randrange(0, 256)
            else:
                state['data_in'] = (state['data_in'] + rng.randrange(1, 4)) & 0xFF
            r2 = rng.random()
            if r2 < 0.3:
                state['match_pattern'] = state['data_in']
            elif r2 < 0.5:
                state['match_pattern'] = rng.randrange(0, 256)
            else:
                state['match_pattern'] = (state['data_in'] ^ rng.randrange(0, 256)) & 0xFF
            state['latch_pattern'] = 1 if rng.random() < 0.2 else 0
        row['data_in'] = state['data_in']
        row['mask'] = state['mask']
        row['match_pattern'] = state['match_pattern']
        row['enable'] = state['enable']
        row['latch_pattern'] = state['latch_pattern']
        if rng.random() < 0.25:
            mid = {}
            if rng.random() < 0.5:
                mid['data_in'] = rng.randrange(0, 256)
                state['data_in'] = mid['data_in']
            if rng.random() < 0.5:
                mid['mask'] = rng.randrange(0, 256)
                state['mask'] = mid['mask']
            if rng.random() < 0.3:
                mid['match_pattern'] = rng.randrange(0, 256)
                state['match_pattern'] = mid['match_pattern']
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows

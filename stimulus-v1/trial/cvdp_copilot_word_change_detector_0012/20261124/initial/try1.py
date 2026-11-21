def stimulus(rng, cycles):
    rows = []
    state = {
        'data_in': 0,
        'mask': 0,
        'match_pattern': 0,
        'enable': 0,
        'latch_pattern': 0,
    }
    reset_cycles = 3
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
        # Occasionally hold values to create long runs
        hold = rng.random() < 0.35
        if not hold:
            # enable mostly on
            state['enable'] = 1 if rng.random() < 0.85 else 0
            # mask: sometimes full, sometimes partial, sometimes zero
            r = rng.random()
            if r < 0.4:
                state['mask'] = 0xFF
            elif r < 0.7:
                state['mask'] = rng.randrange(0, 256)
            else:
                state['mask'] = 0
            # data_in: sometimes repeat previous, sometimes new
            if rng.random() < 0.5:
                state['data_in'] = rng.randrange(0, 256)
            else:
                # small perturbation
                state['data_in'] = (state['data_in'] + rng.randrange(1, 4)) & 0xFF
            # match_pattern: sometimes equal to data_in to trigger match
            r2 = rng.random()
            if r2 < 0.3:
                state['match_pattern'] = state['data_in']
            elif r2 < 0.5:
                state['match_pattern'] = rng.randrange(0, 256)
            else:
                state['match_pattern'] = (state['data_in'] ^ rng.randrange(0, 256)) & 0xFF
            # latch_pattern: pulse occasionally
            state['latch_pattern'] = 1 if rng.random() < 0.15 else 0
        row['data_in'] = state['data_in']
        row['mask'] = state['mask']
        row['match_pattern'] = state['match_pattern']
        row['enable'] = state['enable']
        row['latch_pattern'] = state['latch_pattern']
        # mid overrides: change data_in or mask mid-cycle sometimes
        if rng.random() < 0.2:
            mid = {}
            if rng.random() < 0.5:
                mid['data_in'] = rng.randrange(0, 256)
                state['data_in'] = mid['data_in']
            if rng.random() < 0.5:
                mid['mask'] = rng.randrange(0, 256)
                state['mask'] = mid['mask']
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows

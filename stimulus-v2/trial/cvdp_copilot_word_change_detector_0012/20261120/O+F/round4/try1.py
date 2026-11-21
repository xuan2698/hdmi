def stimulus(rng, cycles):
    rows = []
    data_in = 0
    mask = 0
    match_pattern = 0
    enable = 0
    latch_pattern = 0
    reset = 1
    for c in range(cycles):
        if c < 2:
            reset = 1
            enable = 0
            data_in = 0
            mask = 0
            match_pattern = 0
            latch_pattern = 0
        elif c < 6:
            reset = 0
            enable = 0
            data_in = rng.randrange(256)
            mask = rng.randrange(256)
            match_pattern = rng.randrange(256)
            latch_pattern = rng.randrange(2)
        else:
            reset = 0
            r = rng.random()
            if r < 0.05:
                enable = 0
            else:
                enable = 1
            if rng.random() < 0.20:
                data_in = rng.randrange(256)
            if rng.random() < 0.14:
                mask = rng.randrange(256)
            if rng.random() < 0.14:
                match_pattern = rng.randrange(256)
            latch_pattern = 1 if rng.random() < 0.14 else 0
        row = {
            'reset': reset,
            'data_in': data_in & 0xFF,
            'mask': mask & 0xFF,
            'match_pattern': match_pattern & 0xFF,
            'enable': enable,
            'latch_pattern': latch_pattern,
        }
        mid = {}
        if rng.random() < 0.24:
            mid['data_in'] = rng.randrange(256)
        if rng.random() < 0.14:
            mid['mask'] = rng.randrange(256)
        if rng.random() < 0.14:
            mid['match_pattern'] = rng.randrange(256)
        if rng.random() < 0.07:
            mid['enable'] = rng.randrange(2)
        if rng.random() < 0.07:
            mid['latch_pattern'] = rng.randrange(2)
        if rng.random() < 0.03:
            mid['reset'] = rng.randrange(2)
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows

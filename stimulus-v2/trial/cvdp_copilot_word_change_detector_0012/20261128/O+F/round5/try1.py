def stimulus(rng, cycles):
    rows = []
    data_in = 0
    mask = 0
    match_pattern = 0
    enable = 0
    latch_pattern = 0
    reset = 1
    for i in range(cycles):
        if i < 3:
            reset = 1
            enable = 0
            data_in = 0
            mask = 0
            match_pattern = 0
            latch_pattern = 0
        elif i < 6:
            reset = 0
            enable = 0
            data_in = rng.randrange(256)
            mask = rng.randrange(256)
            match_pattern = rng.randrange(256)
            latch_pattern = rng.randrange(2)
        elif i < 10:
            reset = 0
            enable = 1
            data_in = rng.randrange(256)
            mask = rng.randrange(256)
            match_pattern = rng.randrange(256)
            latch_pattern = 1
        else:
            reset = 0
            r = rng.random()
            if r < 0.05:
                enable = 0
            else:
                enable = 1
            if rng.random() < 0.4:
                data_in = rng.randrange(256)
            if rng.random() < 0.15:
                mask = rng.randrange(256)
            if rng.random() < 0.15:
                match_pattern = rng.randrange(256)
            if rng.random() < 0.2:
                latch_pattern = 1
            else:
                latch_pattern = 0
        row = {
            'reset': reset,
            'data_in': data_in,
            'mask': mask,
            'match_pattern': match_pattern,
            'enable': enable,
            'latch_pattern': latch_pattern,
        }
        if rng.random() < 0.3:
            mid = {}
            if rng.random() < 0.5:
                mid['data_in'] = rng.randrange(256)
            if rng.random() < 0.4:
                mid['mask'] = rng.randrange(256)
            if rng.random() < 0.4:
                mid['match_pattern'] = rng.randrange(256)
            if rng.random() < 0.3:
                mid['enable'] = rng.randrange(2)
            if rng.random() < 0.3:
                mid['latch_pattern'] = rng.randrange(2)
            if rng.random() < 0.1:
                mid['reset'] = rng.randrange(2)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows

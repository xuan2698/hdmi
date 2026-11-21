def stimulus(rng, cycles):
    rows = []
    reset = 1
    data_in = 0
    mask = 0
    match_pattern = 0
    enable = 0
    latch_pattern = 0
    for i in range(4000):
        if i < 2:
            reset = 1
            data_in = 0
            mask = 0
            match_pattern = 0
            enable = 0
            latch_pattern = 0
        elif i < 5:
            reset = 0
            data_in = 0
            mask = 0
            match_pattern = 0
            enable = 0
            latch_pattern = 0
        elif i < 10:
            reset = 0
            data_in = (i * 37) & 0xFF
            mask = 0xFF
            match_pattern = data_in
            enable = 1
            latch_pattern = 1
        else:
            reset = 0
            r = rng.random()
            if r < 0.04:
                enable = 0
            else:
                enable = 1
            if rng.random() < 0.12:
                latch_pattern = 1
            else:
                latch_pattern = 0
            if rng.random() < 0.35:
                data_in = rng.randrange(256)
            if rng.random() < 0.25:
                mask = rng.randrange(256)
            if rng.random() < 0.25:
                match_pattern = rng.randrange(256)
        row = {
            'reset': reset,
            'data_in': data_in,
            'mask': mask,
            'match_pattern': match_pattern,
            'enable': enable,
            'latch_pattern': latch_pattern,
        }
        mid = {}
        if i >= 5 and rng.random() < 0.18:
            if rng.random() < 0.5:
                mid['data_in'] = rng.randrange(256)
            if rng.random() < 0.35:
                mid['mask'] = rng.randrange(256)
            if rng.random() < 0.35:
                mid['match_pattern'] = rng.randrange(256)
            if rng.random() < 0.2:
                mid['enable'] = rng.randrange(2)
            if rng.random() < 0.2:
                mid['latch_pattern'] = rng.randrange(2)
            if rng.random() < 0.05:
                mid['reset'] = 1
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows

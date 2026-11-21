def stimulus(rng, cycles):
    rows = []
    reset = 1
    data_in = 0
    mask = 0
    match_pattern = 0
    enable = 0
    latch_pattern = 0
    for i in range(cycles):
        if i < 3:
            reset = 1
            data_in = 0
            mask = 0
            match_pattern = 0
            enable = 0
            latch_pattern = 0
        elif i == 3:
            reset = 0
            data_in = rng.randrange(256)
            mask = rng.randrange(256)
            match_pattern = rng.randrange(256)
            enable = 1
            latch_pattern = 1
        else:
            reset = 0
            r = rng.random()
            if r < 0.05:
                enable = 0
            elif r < 0.15:
                enable = 1
            if rng.random() < 0.1:
                latch_pattern = 1
            else:
                latch_pattern = 0
            if rng.random() < 0.3:
                data_in = rng.randrange(256)
            if rng.random() < 0.1:
                mask = rng.randrange(256)
            if rng.random() < 0.1:
                match_pattern = rng.randrange(256)
            if rng.random() < 0.02:
                reset = 1
        row = {
            'reset': reset,
            'data_in': data_in & 0xFF,
            'mask': mask & 0xFF,
            'match_pattern': match_pattern & 0xFF,
            'enable': enable & 1,
            'latch_pattern': latch_pattern & 1,
        }
        mid = {}
        if rng.random() < 0.15:
            mid['data_in'] = rng.randrange(256)
        if rng.random() < 0.05:
            mid['mask'] = rng.randrange(256)
        if rng.random() < 0.05:
            mid['match_pattern'] = rng.randrange(256)
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows

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
            data_in = 0
            mask = 0
            match_pattern = 0
            enable = 0
            latch_pattern = 0
        elif i < 10:
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
            else:
                enable = 1
            if rng.random() < 0.10:
                latch_pattern = 1
            else:
                latch_pattern = 0
            if rng.random() < 0.22:
                data_in = rng.randrange(256)
            else:
                if rng.random() < 0.65:
                    data_in = (data_in + rng.randrange(1, 4)) & 0xFF
            if rng.random() < 0.15:
                mask = rng.randrange(256)
            if rng.random() < 0.15:
                match_pattern = rng.randrange(256)
            if rng.random() < 0.14:
                match_pattern = data_in
            if rng.random() < 0.07:
                mask = 0xFF
            if rng.random() < 0.07:
                mask = 0x00
            if rng.random() < 0.05:
                data_in = 0
            if rng.random() < 0.05:
                data_in = 0xFF
        mid = None
        if i >= 10 and rng.random() < 0.40:
            mid = {}
            if rng.random() < 0.55:
                mid['data_in'] = rng.randrange(256)
            if rng.random() < 0.35:
                mid['mask'] = rng.randrange(256)
            if rng.random() < 0.35:
                mid['match_pattern'] = rng.randrange(256)
            if rng.random() < 0.25:
                mid['latch_pattern'] = rng.randrange(2)
            if rng.random() < 0.25:
                mid['enable'] = rng.randrange(2)
            if rng.random() < 0.10:
                mid['reset'] = 1
        row = {
            'reset': reset,
            'data_in': data_in & 0xFF,
            'mask': mask & 0xFF,
            'match_pattern': match_pattern & 0xFF,
            'enable': enable & 1,
            'latch_pattern': latch_pattern & 1,
        }
        if mid is not None:
            row['mid'] = mid
        rows.append(row)
    return rows

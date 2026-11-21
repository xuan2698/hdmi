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
        elif i < 6:
            reset = 0
            data_in = rng.randrange(256)
            mask = 0xFF
            match_pattern = data_in
            enable = 1
            latch_pattern = 1
        elif i < 10:
            reset = 0
            enable = 1
            latch_pattern = 0
            mask = 0xFF
            data_in = (data_in + 1) & 0xFF
            match_pattern = data_in
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
            if rng.random() < 0.30:
                data_in = rng.randrange(256)
            else:
                if rng.random() < 0.5:
                    data_in = (data_in + rng.randrange(1, 4)) & 0xFF
                else:
                    data_in = data_in & 0xFF
            if rng.random() < 0.15:
                mask = rng.randrange(256)
            if rng.random() < 0.15:
                match_pattern = rng.randrange(256)
            if rng.random() < 0.10:
                match_pattern = data_in
            if rng.random() < 0.06:
                mask = 0xFF
                match_pattern = data_in
        mid = None
        if i >= 10 and rng.random() < 0.30:
            mid = {}
            if rng.random() < 0.5:
                mid['data_in'] = rng.randrange(256)
            if rng.random() < 0.3:
                mid['mask'] = rng.randrange(256)
            if rng.random() < 0.3:
                mid['match_pattern'] = rng.randrange(256)
            if rng.random() < 0.2:
                mid['latch_pattern'] = rng.randrange(2)
            if rng.random() < 0.2:
                mid['enable'] = rng.randrange(2)
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

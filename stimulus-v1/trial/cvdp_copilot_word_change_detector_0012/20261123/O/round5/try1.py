def stimulus(rng, cycles):
    rows = []
    data_in = 0
    mask = 0
    match_pattern = 0
    enable = 0
    latch_pattern = 0
    reset = 1
    for i in range(cycles):
        if i < 4:
            reset = 1
            data_in = 0
            mask = 0
            match_pattern = 0
            enable = 0
            latch_pattern = 0
        else:
            reset = 0
            if i == 4:
                enable = 1
                mask = 0xFF
                latch_pattern = 1
                match_pattern = rng.randrange(256)
                data_in = rng.randrange(256)
            elif i < 12:
                enable = 1
                latch_pattern = 0
                data_in = rng.randrange(256)
                mask = 0xFF
                match_pattern = rng.randrange(256)
            elif i < 20:
                enable = 1
                latch_pattern = 0
                mask = rng.randrange(256)
                data_in = rng.randrange(256)
                match_pattern = rng.randrange(256)
            else:
                r = rng.random()
                if r < 0.04:
                    enable = 1 - enable
                if rng.random() < 0.08:
                    latch_pattern = 1
                    match_pattern = rng.randrange(256)
                else:
                    latch_pattern = 0
                if rng.random() < 0.35:
                    data_in = rng.randrange(256)
                if rng.random() < 0.12:
                    mask = rng.randrange(256)
                if rng.random() < 0.06:
                    match_pattern = rng.randrange(256)
                if rng.random() < 0.02:
                    reset = 1
        row = {
            'reset': reset & 1,
            'data_in': data_in & 0xFF,
            'mask': mask & 0xFF,
            'match_pattern': match_pattern & 0xFF,
            'enable': enable & 1,
            'latch_pattern': latch_pattern & 1,
        }
        mid = {}
        if i >= 4 and reset == 0:
            if rng.random() < 0.18:
                mid['data_in'] = rng.randrange(256)
            if rng.random() < 0.08:
                mid['mask'] = rng.randrange(256)
            if rng.random() < 0.08:
                mid['match_pattern'] = rng.randrange(256)
            if rng.random() < 0.04:
                mid['latch_pattern'] = rng.randrange(2)
            if rng.random() < 0.04:
                mid['enable'] = rng.randrange(2)
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows

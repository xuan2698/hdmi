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
            r = rng.random()
            if r < 0.04:
                enable = 0
            else:
                enable = 1
            if rng.random() < 0.18:
                latch_pattern = 1
            else:
                latch_pattern = 0
            if rng.random() < 0.35:
                data_in = rng.randrange(256)
            if rng.random() < 0.22:
                mask = rng.randrange(256)
            if rng.random() < 0.22:
                match_pattern = rng.randrange(256)
            if i > 8 and rng.random() < 0.18:
                data_in = (data_in + 1) & 0xFF
            if i > 16 and rng.random() < 0.12:
                data_in = (data_in ^ 0x01) & 0xFF
            if i > 24 and rng.random() < 0.08:
                mask = 0xFF
                match_pattern = data_in
                latch_pattern = 1
            if i > 32 and rng.random() < 0.06:
                mask = 0x00
            if i > 40 and rng.random() < 0.05:
                mask = 0xFF
                match_pattern = rng.randrange(256)
                latch_pattern = 1
            if i > 48 and rng.random() < 0.05:
                data_in = 0
                mask = 0xFF
                match_pattern = 0
                latch_pattern = 1
            if i > 56 and rng.random() < 0.04:
                data_in = 0xFF
                mask = 0xFF
                match_pattern = 0xFF
                latch_pattern = 1
        row = {
            'reset': reset,
            'data_in': data_in & 0xFF,
            'mask': mask & 0xFF,
            'match_pattern': match_pattern & 0xFF,
            'enable': enable & 1,
            'latch_pattern': latch_pattern & 1,
        }
        mid = {}
        if reset == 0 and enable == 1:
            if rng.random() < 0.28:
                mid['data_in'] = rng.randrange(256)
            if rng.random() < 0.12:
                mid['mask'] = rng.randrange(256)
            if rng.random() < 0.12:
                mid['match_pattern'] = rng.randrange(256)
            if rng.random() < 0.06:
                mid['latch_pattern'] = rng.randrange(2)
            if rng.random() < 0.04:
                mid['enable'] = 0
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows

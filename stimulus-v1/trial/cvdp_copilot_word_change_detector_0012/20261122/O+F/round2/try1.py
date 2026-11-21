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
            if r < 0.06:
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
            if i > 10 and rng.random() < 0.12:
                data_in = (data_in + 1) & 0xFF
            if i > 20 and rng.random() < 0.08:
                data_in = (data_in ^ 0x01) & 0xFF
            if i > 30 and rng.random() < 0.05:
                mask = 0xFF
                match_pattern = data_in
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

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
            if r < 0.05:
                enable = 0
            else:
                enable = 1
            if rng.random() < 0.15:
                latch_pattern = 1
            else:
                latch_pattern = 0
            if rng.random() < 0.30:
                data_in = rng.randrange(256)
            if rng.random() < 0.20:
                mask = rng.randrange(256)
            if rng.random() < 0.20:
                match_pattern = rng.randrange(256)
            if i > 10 and rng.random() < 0.15:
                data_in = (data_in + 1) & 0xFF
            if i > 20 and rng.random() < 0.10:
                data_in = (data_in ^ 0x01) & 0xFF
            if i > 30 and rng.random() < 0.06:
                mask = 0xFF
                match_pattern = data_in
            if i > 40 and rng.random() < 0.05:
                mask = 0x00
            if i > 50 and rng.random() < 0.04:
                mask = 0xFF
                match_pattern = rng.randrange(256)
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
            if rng.random() < 0.25:
                mid['data_in'] = rng.randrange(256)
            if rng.random() < 0.10:
                mid['mask'] = rng.randrange(256)
            if rng.random() < 0.10:
                mid['match_pattern'] = rng.randrange(256)
            if rng.random() < 0.05:
                mid['latch_pattern'] = rng.randrange(2)
            if rng.random() < 0.03:
                mid['enable'] = 0
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows

def stimulus(rng, cycles):
    rows = []
    data_in = 0
    mask = 0
    match_pattern = 0
    enable = 0
    latch_pattern = 0
    reset = 1
    for i in range(cycles):
        if i < 6:
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
            if rng.random() < 0.20:
                latch_pattern = 1
            else:
                latch_pattern = 0
            if rng.random() < 0.50:
                data_in = rng.randrange(256)
            if rng.random() < 0.25:
                mask = rng.randrange(256)
            if rng.random() < 0.25:
                match_pattern = rng.randrange(256)
            if i > 12 and rng.random() < 0.20:
                data_in = (data_in + 1) & 0xFF
            if i > 16 and rng.random() < 0.14:
                mask = (mask ^ (1 << rng.randrange(8))) & 0xFF
            if i > 20 and rng.random() < 0.12:
                match_pattern = (match_pattern + 1) & 0xFF
            if i > 24 and rng.random() < 0.10:
                data_in = (data_in ^ (1 << rng.randrange(8))) & 0xFF
            if i > 30 and rng.random() < 0.07:
                mask = 0xFF
            if i > 34 and rng.random() < 0.07:
                mask = 0x00
            if i > 40 and rng.random() < 0.06:
                data_in = match_pattern
            if i > 50 and rng.random() < 0.05:
                data_in = (data_in + 0x10) & 0xFF
            if i > 60 and rng.random() < 0.05:
                mask = (mask | 0x0F) & 0xFF
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
            if rng.random() < 0.30:
                mid['data_in'] = rng.randrange(256)
            if rng.random() < 0.14:
                mid['mask'] = rng.randrange(256)
            if rng.random() < 0.14:
                mid['match_pattern'] = rng.randrange(256)
            if rng.random() < 0.08:
                mid['latch_pattern'] = rng.randrange(2)
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows

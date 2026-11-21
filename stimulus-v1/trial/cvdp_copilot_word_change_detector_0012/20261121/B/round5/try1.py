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
        elif i < 8:
            reset = 0
            data_in = (i * 37) & 0xFF
            mask = 0xFF
            match_pattern = data_in
            enable = 1
            latch_pattern = 1
        elif i < 14:
            reset = 0
            enable = 1
            latch_pattern = 0
            data_in = (data_in + 1) & 0xFF
            mask = 0xFF
            match_pattern = data_in
        elif i < 20:
            reset = 0
            enable = 1
            latch_pattern = 0
            data_in = (data_in ^ 0x55) & 0xFF
            mask = 0x0F
            match_pattern = (match_pattern + 3) & 0xFF
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
            else:
                step = rng.randrange(1, 5)
                if rng.random() < 0.5:
                    data_in = (data_in + step) & 0xFF
                else:
                    data_in = (data_in - step) & 0xFF
            if rng.random() < 0.18:
                mask = rng.randrange(256)
            if rng.random() < 0.18:
                match_pattern = rng.randrange(256)
            if rng.random() < 0.12:
                match_pattern = data_in
            if rng.random() < 0.08:
                mask = 0xFF
            if rng.random() < 0.06:
                mask = 0x00
            if rng.random() < 0.05:
                mask = 0xF0
            if rng.random() < 0.05:
                mask = 0x0F
            if rng.random() < 0.05:
                mask = 0xAA
            if rng.random() < 0.05:
                mask = 0x55
        mid = None
        if i >= 20 and rng.random() < 0.45:
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
        row = {
            'reset': reset & 1,
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

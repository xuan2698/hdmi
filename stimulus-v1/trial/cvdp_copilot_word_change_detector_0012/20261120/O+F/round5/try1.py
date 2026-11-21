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
            data_in = 0
            mask = 0xFF
            match_pattern = 0xA5
            enable = 1
            latch_pattern = 1
        elif i < 10:
            reset = 0
            enable = 1
            latch_pattern = 0
            data_in = (data_in + 0x11) & 0xFF
            mask = 0xFF
        elif i < 18:
            reset = 0
            enable = 1
            latch_pattern = 0
            data_in = 0xA5
            mask = 0xFF
        elif i < 26:
            reset = 0
            enable = 1
            latch_pattern = 0
            data_in = rng.randrange(256)
            mask = 0xFF
        elif i < 34:
            reset = 0
            enable = 1
            latch_pattern = 0
            data_in = 0xA5
            mask = 0xFF
        elif i < 60:
            reset = 0
            enable = 1
            latch_pattern = 0
            if rng.random() < 0.5:
                data_in = rng.randrange(256)
            if rng.random() < 0.2:
                mask = rng.randrange(256)
            if rng.random() < 0.1:
                match_pattern = rng.randrange(256)
        else:
            reset = 0
            r = rng.random()
            if r < 0.04:
                enable = 0
            elif r < 0.12:
                enable = 1
            if rng.random() < 0.08:
                latch_pattern = 1
            else:
                latch_pattern = 0
            if rng.random() < 0.35:
                data_in = rng.randrange(256)
            if rng.random() < 0.12:
                mask = rng.randrange(256)
            if rng.random() < 0.12:
                match_pattern = rng.randrange(256)
            if rng.random() < 0.015:
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
        if rng.random() < 0.18:
            mid['data_in'] = rng.randrange(256)
        if rng.random() < 0.06:
            mid['mask'] = rng.randrange(256)
        if rng.random() < 0.06:
            mid['match_pattern'] = rng.randrange(256)
        if rng.random() < 0.04:
            mid['enable'] = rng.randrange(2)
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows

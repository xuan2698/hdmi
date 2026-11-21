def stimulus(rng, cycles):
    rows = []
    data_in = 0
    mask = 0
    match_pattern = 0
    enable = 0
    latch_pattern = 0
    reset = 1
    latched = 0
    for i in range(cycles):
        if i < 3:
            reset = 1
            data_in = 0
            mask = 0
            match_pattern = 0
            enable = 0
            latch_pattern = 0
        else:
            reset = 0
            if i == 3:
                enable = 1
                mask = 0xFF
                match_pattern = 0xA5
                latch_pattern = 1
                data_in = 0x00
            elif i == 4:
                latch_pattern = 0
                data_in = 0xA5
            elif i == 5:
                data_in = 0x5A
            elif i == 6:
                data_in = 0xA5
            elif i == 7:
                mask = 0x0F
                data_in = 0xAF
            elif i == 8:
                data_in = 0xA0
            elif i == 9:
                enable = 0
                data_in = 0x11
            elif i == 10:
                enable = 1
                mask = 0xFF
                data_in = 0xA5
            else:
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
                if rng.random() < 0.18:
                    mask = rng.randrange(256)
                if rng.random() < 0.18:
                    match_pattern = rng.randrange(256)
                if i > 15 and rng.random() < 0.10:
                    data_in = (data_in + 1) & 0xFF
                if i > 25 and rng.random() < 0.08:
                    data_in = (data_in - 1) & 0xFF
                if i > 35 and rng.random() < 0.06:
                    mask = (mask ^ 0xFF) & 0xFF
                if i > 45 and rng.random() < 0.05:
                    match_pattern = (match_pattern + 1) & 0xFF
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

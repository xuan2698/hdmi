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
                match_pattern = 0xA5
                latch_pattern = 1
                data_in = 0x00
            elif i == 5:
                latch_pattern = 0
                data_in = 0xA5
            elif i == 6:
                data_in = 0x5A
            elif i == 7:
                data_in = 0xA5
            elif i == 8:
                mask = 0x0F
                data_in = 0xAF
            elif i == 9:
                data_in = 0xA0
            elif i == 10:
                enable = 0
                data_in = 0x11
            elif i == 11:
                enable = 1
                mask = 0xFF
                data_in = 0xA5
            elif i == 12:
                data_in = 0xA5
            elif i == 13:
                data_in = 0xA5
            elif i == 14:
                mask = 0x00
                data_in = 0x3C
            elif i == 15:
                mask = 0xFF
                data_in = 0x3C
            elif i == 16:
                latch_pattern = 1
                match_pattern = 0x3C
            elif i == 17:
                latch_pattern = 0
                data_in = 0x3C
            elif i == 18:
                data_in = 0xC3
            elif i == 19:
                data_in = 0x3C
            else:
                r = rng.random()
                if r < 0.04:
                    enable = 0
                else:
                    enable = 1
                if rng.random() < 0.12:
                    latch_pattern = 1
                else:
                    latch_pattern = 0
                if rng.random() < 0.28:
                    data_in = rng.randrange(256)
                if rng.random() < 0.15:
                    mask = rng.randrange(256)
                if rng.random() < 0.15:
                    match_pattern = rng.randrange(256)
                if i > 25 and rng.random() < 0.10:
                    data_in = (data_in + 1) & 0xFF
                if i > 35 and rng.random() < 0.08:
                    data_in = (data_in - 1) & 0xFF
                if i > 45 and rng.random() < 0.06:
                    mask = (mask ^ 0xFF) & 0xFF
                if i > 55 and rng.random() < 0.05:
                    match_pattern = (match_pattern + 1) & 0xFF
                if i > 65 and rng.random() < 0.05:
                    data_in = (data_in ^ 0xFF) & 0xFF
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
            if rng.random() < 0.22:
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

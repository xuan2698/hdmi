def stimulus(rng, cycles):
    rows = []
    reset = 1
    data_in = 0
    mask = 0
    match_pattern = 0
    enable = 0
    latch_pattern = 0
    for i in range(cycles):
        mid = None
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
            match_pattern = 0
            enable = 1
            latch_pattern = 1
        elif i == 4:
            reset = 0
            data_in = 0x5A
            mask = 0xFF
            match_pattern = 0x5A
            enable = 1
            latch_pattern = 1
            mid = {'data_in': 0xA5}
        elif i == 5:
            reset = 0
            data_in = 0xA5
            mask = 0xFF
            match_pattern = 0x5A
            enable = 1
            latch_pattern = 0
        elif i == 6:
            reset = 0
            data_in = 0x5A
            mask = 0xFF
            match_pattern = 0x5A
            enable = 1
            latch_pattern = 0
        elif i == 7:
            reset = 0
            data_in = 0x00
            mask = 0x0F
            match_pattern = 0x00
            enable = 1
            latch_pattern = 0
        elif i == 8:
            reset = 0
            data_in = 0xFF
            mask = 0x0F
            match_pattern = 0x00
            enable = 1
            latch_pattern = 0
        elif i == 9:
            reset = 0
            data_in = 0xFF
            mask = 0x0F
            match_pattern = 0x00
            enable = 0
            latch_pattern = 0
        elif i == 10:
            reset = 0
            data_in = 0x00
            mask = 0x0F
            match_pattern = 0x00
            enable = 1
            latch_pattern = 0
        elif i == 11:
            reset = 1
            data_in = 0x00
            mask = 0x00
            match_pattern = 0x00
            enable = 1
            latch_pattern = 0
            mid = {'reset': 0, 'enable': 1}
        else:
            reset = 0
            r = rng.random()
            if r < 0.03:
                enable = 1 - enable
            if rng.random() < 0.12:
                latch_pattern = 1
            else:
                latch_pattern = 0
            if rng.random() < 0.40:
                data_in = rng.randrange(256)
            if rng.random() < 0.10:
                mask = rng.randrange(256)
            if rng.random() < 0.10:
                match_pattern = rng.randrange(256)
            if rng.random() < 0.015:
                reset = 1
            if rng.random() < 0.06:
                mid = {'data_in': rng.randrange(256)}
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

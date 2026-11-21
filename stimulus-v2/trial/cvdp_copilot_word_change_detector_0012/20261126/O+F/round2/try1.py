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
        if i < 2:
            reset = 1
            data_in = 0
            mask = 0
            match_pattern = 0
            enable = 0
            latch_pattern = 0
        elif i < 5:
            reset = 0
            data_in = rng.randrange(256)
            mask = rng.randrange(256)
            match_pattern = rng.randrange(256)
            enable = 1
            latch_pattern = 1
        else:
            reset = 0
            r = rng.random()
            if r < 0.06:
                data_in = rng.randrange(256)
            elif r < 0.12:
                data_in = (data_in + rng.randrange(1, 4)) & 0xFF
            elif r < 0.18:
                data_in = (data_in ^ (1 << rng.randrange(8))) & 0xFF
            if rng.random() < 0.04:
                mask = rng.randrange(256)
            if rng.random() < 0.04:
                match_pattern = rng.randrange(256)
            if rng.random() < 0.02:
                enable = 1 - enable
            if rng.random() < 0.06:
                latch_pattern = 1
            else:
                latch_pattern = 0
            if rng.random() < 0.03:
                mid = {'reset': 1, 'data_in': 0, 'enable': 0}
            elif rng.random() < 0.03:
                mid = {'mask': rng.randrange(256), 'latch_pattern': 0}
            elif rng.random() < 0.03:
                mid = {'enable': 1 - enable, 'latch_pattern': 1}
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

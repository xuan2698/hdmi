def stimulus(rng, cycles):
    rows = []
    reset = 1
    data_in = 0
    mask = 0
    match_pattern = 0
    enable = 0
    latch_pattern = 0
    for i in range(cycles):
        if i < 4:
            reset = 1
            data_in = 0
            mask = 0
            match_pattern = 0
            enable = 0
            latch_pattern = 0
        elif i < 8:
            reset = 0
            data_in = rng.randrange(256)
            mask = rng.randrange(256)
            match_pattern = rng.randrange(256)
            enable = 1
            latch_pattern = 1
        else:
            reset = 0
            r = rng.random()
            if r < 0.08:
                data_in = rng.randrange(256)
            elif r < 0.16:
                data_in = (data_in + rng.randrange(1, 5)) % 256
            elif r < 0.24:
                data_in = (data_in ^ (1 << rng.randrange(8))) % 256
            elif r < 0.28:
                data_in = 0
            if rng.random() < 0.05:
                mask = rng.randrange(256)
            if rng.random() < 0.05:
                match_pattern = rng.randrange(256)
            if rng.random() < 0.03:
                enable = 1 - enable
            if rng.random() < 0.08:
                latch_pattern = 1
            else:
                latch_pattern = 0
        row = {
            'reset': reset,
            'data_in': data_in & 0xFF,
            'mask': mask & 0xFF,
            'match_pattern': match_pattern & 0xFF,
            'enable': enable & 1,
            'latch_pattern': latch_pattern & 1,
        }
        rows.append(row)
    return rows

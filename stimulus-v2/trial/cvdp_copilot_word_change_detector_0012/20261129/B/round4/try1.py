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
            enable = 0
            latch_pattern = 0
            data_in = 0
            mask = 0
            match_pattern = 0
        elif i < 8:
            reset = 0
            enable = 0
            latch_pattern = 0
        else:
            reset = 0
            if i % 131 == 0:
                enable = 1
                latch_pattern = 1
                match_pattern = rng.randrange(256)
                mask = rng.randrange(256)
                data_in = rng.randrange(256)
            elif i % 89 == 0:
                enable = 1
                latch_pattern = 0
                data_in = rng.randrange(256)
                mask = rng.randrange(256)
            elif i % 17 == 0:
                enable = 1
                latch_pattern = 0
                data_in = rng.randrange(256)
            elif i % 11 == 0:
                enable = 0
                latch_pattern = 0
            elif i % 5 == 0:
                enable = 1
                latch_pattern = 0
                if rng.randrange(3) == 0:
                    data_in = rng.randrange(256)
                if rng.randrange(6) == 0:
                    mask = rng.randrange(256)
            else:
                enable = 1
                latch_pattern = 0
                if rng.randrange(5) == 0:
                    data_in = rng.randrange(256)
                if rng.randrange(9) == 0:
                    mask = rng.randrange(256)
        row = {
            'reset': reset & 1,
            'data_in': data_in & 0xFF,
            'mask': mask & 0xFF,
            'match_pattern': match_pattern & 0xFF,
            'enable': enable & 1,
            'latch_pattern': latch_pattern & 1,
        }
        rows.append(row)
    return rows

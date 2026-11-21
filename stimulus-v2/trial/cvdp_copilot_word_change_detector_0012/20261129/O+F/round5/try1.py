def stimulus(rng, cycles):
    rows = []
    data_in = 0
    mask = 0
    match_pattern = 0
    enable = 0
    latch_pattern = 0
    reset = 1
    for i in range(cycles):
        mid = None
        if i < 3:
            reset = 1
            enable = 0
            latch_pattern = 0
        elif i < 6:
            reset = 0
            enable = 1
            latch_pattern = 0
            if i == 3:
                data_in = 8
                mask = 0
                match_pattern = 0
            elif i == 4:
                data_in = 0
                mask = 8
                match_pattern = 0
            else:
                data_in = 0
                mask = 0
                match_pattern = 0
        else:
            reset = 0
            if i % 97 == 0:
                enable = 1
                latch_pattern = 1
                match_pattern = rng.randrange(256)
                mask = rng.randrange(256)
                data_in = rng.randrange(256)
            elif i % 13 == 0:
                enable = 1
                latch_pattern = 0
                data_in = rng.randrange(256)
                mask = rng.randrange(256)
            elif i % 7 == 0:
                enable = 1
                latch_pattern = 0
                data_in = rng.randrange(256)
            elif i % 5 == 0:
                enable = 0
                latch_pattern = 0
            else:
                enable = 1
                latch_pattern = 0
                if rng.randrange(4) == 0:
                    data_in = rng.randrange(256)
                if rng.randrange(8) == 0:
                    mask = rng.randrange(256)
        if i == 1:
            mid = {'enable': 1, 'latch_pattern': 1}
        elif i == 2:
            mid = {'reset': 1, 'data_in': 0, 'enable': 0}
        elif i == 3:
            mid = {'mask': 0, 'latch_pattern': 0}
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

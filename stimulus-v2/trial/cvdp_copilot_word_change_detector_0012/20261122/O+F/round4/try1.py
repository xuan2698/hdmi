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
        if i < 2:
            reset = 1
            enable = 0
            latch_pattern = 0
            data_in = 0
            mask = 0
            match_pattern = 0
        elif i == 2:
            reset = 1
            enable = 0
            latch_pattern = 0
            data_in = 0
            mask = 0
            match_pattern = 0
            mid = {'reset': 0, 'data_in': 8, 'enable': 1, 'latch_pattern': 1}
        elif i == 3:
            reset = 0
            data_in = 0
            mask = 8
            match_pattern = 0
            enable = 1
            latch_pattern = 1
            mid = {'mask': 0, 'latch_pattern': 0}
        elif i == 4:
            reset = 0
            data_in = 0
            mask = 0
            match_pattern = 0
            enable = 1
            latch_pattern = 1
        elif i < 12:
            reset = 0
            enable = 1
            latch_pattern = 1 if rng.randrange(3) == 0 else 0
            data_in = rng.randrange(256)
            mask = rng.randrange(256)
            match_pattern = rng.randrange(256)
        elif i < 40:
            reset = 0
            enable = 1
            latch_pattern = 0
            if rng.randrange(2) == 0:
                data_in = rng.randrange(256)
            if rng.randrange(3) == 0:
                mask = rng.randrange(256)
            if rng.randrange(4) == 0:
                match_pattern = rng.randrange(256)
        elif i < 120:
            reset = 0
            enable = 1 if rng.randrange(8) != 0 else 0
            latch_pattern = 1 if rng.randrange(15) == 0 else 0
            if rng.randrange(2) == 0:
                data_in = rng.randrange(256)
            if rng.randrange(3) == 0:
                mask = rng.randrange(256)
            if rng.randrange(5) == 0:
                match_pattern = rng.randrange(256)
        elif i < 400:
            reset = 0
            enable = 1
            latch_pattern = 0
            if rng.randrange(2) == 0:
                data_in = rng.randrange(256)
            if rng.randrange(4) == 0:
                mask = rng.randrange(256)
            if rng.randrange(6) == 0:
                match_pattern = rng.randrange(256)
        elif i < 1200:
            reset = 0
            enable = 1 if rng.randrange(6) != 0 else 0
            latch_pattern = 1 if rng.randrange(12) == 0 else 0
            if rng.randrange(2) == 0:
                data_in = rng.randrange(256)
            if rng.randrange(3) == 0:
                mask = rng.randrange(256)
            if rng.randrange(5) == 0:
                match_pattern = rng.randrange(256)
        elif i < 2500:
            reset = 0
            enable = 1
            latch_pattern = 0
            if rng.randrange(2) == 0:
                data_in = rng.randrange(256)
            if rng.randrange(3) == 0:
                mask = rng.randrange(256)
            if rng.randrange(4) == 0:
                match_pattern = rng.randrange(256)
        else:
            reset = 0
            enable = 1 if rng.randrange(5) != 0 else 0
            latch_pattern = 1 if rng.randrange(10) == 0 else 0
            if rng.randrange(2) == 0:
                data_in = rng.randrange(256)
            if rng.randrange(3) == 0:
                mask = rng.randrange(256)
            if rng.randrange(4) == 0:
                match_pattern = rng.randrange(256)
        row = {
            'reset': reset,
            'data_in': data_in,
            'mask': mask,
            'match_pattern': match_pattern,
            'enable': enable,
            'latch_pattern': latch_pattern,
        }
        if mid is not None:
            row['mid'] = mid
        rows.append(row)
    return rows

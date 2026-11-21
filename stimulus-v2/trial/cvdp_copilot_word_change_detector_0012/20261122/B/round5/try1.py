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
            enable = 0
            latch_pattern = 0
            data_in = 0
            mask = 0
            match_pattern = 0
        else:
            reset = 0
            if i == 3:
                enable = 1
                latch_pattern = 1
                data_in = rng.randrange(256)
                mask = rng.randrange(256)
                match_pattern = rng.randrange(256)
            elif i < 10:
                enable = 1
                latch_pattern = 0
                data_in = rng.randrange(256)
                mask = rng.randrange(256)
                match_pattern = rng.randrange(256)
            elif i < 20:
                enable = 1
                latch_pattern = 1 if rng.randrange(4) == 0 else 0
                data_in = rng.randrange(256)
                mask = rng.randrange(256)
                match_pattern = rng.randrange(256)
            elif i < 100:
                enable = 1
                latch_pattern = 0
                if rng.randrange(3) == 0:
                    data_in = rng.randrange(256)
                if rng.randrange(5) == 0:
                    mask = rng.randrange(256)
                if rng.randrange(7) == 0:
                    match_pattern = rng.randrange(256)
            elif i < 200:
                enable = 1 if rng.randrange(10) != 0 else 0
                latch_pattern = 1 if rng.randrange(20) == 0 else 0
                if rng.randrange(2) == 0:
                    data_in = rng.randrange(256)
                if rng.randrange(4) == 0:
                    mask = rng.randrange(256)
                if rng.randrange(6) == 0:
                    match_pattern = rng.randrange(256)
            elif i < 500:
                enable = 1
                latch_pattern = 0
                if rng.randrange(2) == 0:
                    data_in = rng.randrange(256)
                if rng.randrange(3) == 0:
                    mask = rng.randrange(256)
                if rng.randrange(5) == 0:
                    match_pattern = rng.randrange(256)
            elif i < 1000:
                enable = 1 if rng.randrange(8) != 0 else 0
                latch_pattern = 1 if rng.randrange(15) == 0 else 0
                if rng.randrange(2) == 0:
                    data_in = rng.randrange(256)
                if rng.randrange(3) == 0:
                    mask = rng.randrange(256)
                if rng.randrange(4) == 0:
                    match_pattern = rng.randrange(256)
            elif i < 2000:
                enable = 1
                latch_pattern = 0
                if rng.randrange(2) == 0:
                    data_in = rng.randrange(256)
                if rng.randrange(4) == 0:
                    mask = rng.randrange(256)
                if rng.randrange(6) == 0:
                    match_pattern = rng.randrange(256)
            elif i < 5000:
                enable = 1 if rng.randrange(6) != 0 else 0
                latch_pattern = 1 if rng.randrange(12) == 0 else 0
                if rng.randrange(2) == 0:
                    data_in = rng.randrange(256)
                if rng.randrange(3) == 0:
                    mask = rng.randrange(256)
                if rng.randrange(5) == 0:
                    match_pattern = rng.randrange(256)
            elif i < 10000:
                enable = 1
                latch_pattern = 0
                if rng.randrange(2) == 0:
                    data_in = rng.randrange(256)
                if rng.randrange(3) == 0:
                    mask = rng.randrange(256)
                if rng.randrange(4) == 0:
                    match_pattern = rng.randrange(256)
            else:
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
        rows.append(row)
    return rows

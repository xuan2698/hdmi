def stimulus(rng, cycles):
    rows = []
    data_in = 0
    mask = 0
    match_pattern = 0
    enable = 0
    latch_pattern = 0
    for i in range(cycles):
        row = {}
        if i < 3:
            row['reset'] = 1
            row['data_in'] = 0
            row['mask'] = 0
            row['match_pattern'] = 0
            row['enable'] = 0
            row['latch_pattern'] = 0
            rows.append(row)
            continue
        row['reset'] = 0
        phase = i % 48
        if phase < 4:
            enable = 1
            mask = 0xFF
            data_in = (data_in + 1) & 0xFF
            match_pattern = data_in
            latch_pattern = 1 if phase == 0 else 0
        elif phase < 10:
            enable = 1
            mask = 0xFF
            data_in = (data_in + 1) & 0xFF
            match_pattern = data_in
            latch_pattern = 0
        elif phase < 16:
            enable = 1
            mask = rng.choice([0x0F, 0xF0, 0xAA, 0x55, 0xFF, 0x00])
            data_in = rng.randrange(0, 256)
            match_pattern = data_in
            latch_pattern = 1 if phase == 10 else 0
        elif phase < 22:
            enable = 1
            mask = 0xFF
            data_in = rng.randrange(0, 256)
            match_pattern = rng.randrange(0, 256)
            latch_pattern = 0
        elif phase < 28:
            enable = 0
            mask = rng.randrange(0, 256)
            data_in = rng.randrange(0, 256)
            match_pattern = rng.randrange(0, 256)
            latch_pattern = 0
        elif phase < 34:
            enable = 1
            mask = 0
            data_in = rng.randrange(0, 256)
            match_pattern = rng.randrange(0, 256)
            latch_pattern = 1 if phase == 28 else 0
        elif phase < 40:
            enable = 1
            mask = 0xFF
            data_in = (data_in + rng.randrange(1, 4)) & 0xFF
            match_pattern = data_in
            latch_pattern = 0
        else:
            enable = 1
            mask = rng.choice([0x0F, 0xF0, 0xAA, 0x55])
            data_in = rng.randrange(0, 256)
            match_pattern = data_in & mask
            latch_pattern = 1 if phase == 40 else 0
        row['data_in'] = data_in
        row['mask'] = mask
        row['match_pattern'] = match_pattern
        row['enable'] = enable
        row['latch_pattern'] = latch_pattern
        if rng.random() < 0.25:
            mid = {}
            if rng.random() < 0.6:
                mid['data_in'] = rng.randrange(0, 256)
                data_in = mid['data_in']
            if rng.random() < 0.4:
                mid['mask'] = rng.randrange(0, 256)
                mask = mid['mask']
            if rng.random() < 0.3:
                mid['match_pattern'] = rng.randrange(0, 256)
                match_pattern = mid['match_pattern']
            if rng.random() < 0.2:
                mid['latch_pattern'] = rng.randrange(0, 2)
                latch_pattern = mid['latch_pattern']
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows

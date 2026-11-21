def stimulus(rng, cycles):
    rows = []
    # Directed prefix: reset, then walk through all four nodes with data toggling.
    seq = [
        (1, 0, 0),   # async reset
        (0, 0, 0),   # NODE0 idle
        (0, 5, 1),   # NODE0 send
        (0, 0xA, 0), # NODE1 idle
        (0, 0xF, 1), # NODE1 send
        (0, 3, 1),   # NODE2 send
        (0, 0, 0),   # NODE2 idle
        (0, 7, 1),   # NODE3 send
        (0, 0xC, 0), # NODE3 idle
        (0, 1, 1),   # NODE0 send
        (1, 9, 1),   # reset mid-stream
        (0, 2, 0),
        (0, 4, 1),
        (0, 8, 1),
        (0, 6, 0),
        (0, 0xE, 1),
    ]
    for r, d, h in seq:
        if len(rows) >= cycles:
            break
        rows.append({'rst': r, 'data_in': d & 0xF, 'has_data_to_send': h & 1})

    # Fill remaining with structured random exploration.
    while len(rows) < cycles:
        i = len(rows)
        # Occasionally inject reset to test async behavior at various states.
        if i % 37 == 0:
            r = 1
        else:
            r = 0
        # Bias has_data_to_send to exercise both idle and send paths.
        h = 1 if (i % 3 != 0) else 0
        if rng.random() < 0.15:
            h = 1 - h
        d = rng.randrange(16)
        row = {'rst': r, 'data_in': d, 'has_data_to_send': h}
        # Mid-cycle changes on some rows to stress timing.
        if rng.random() < 0.2:
            mid = {}
            if rng.random() < 0.5:
                mid['has_data_to_send'] = 1 - h
            if rng.random() < 0.5:
                mid['data_in'] = rng.randrange(16)
            if rng.random() < 0.1:
                mid['rst'] = 1
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows

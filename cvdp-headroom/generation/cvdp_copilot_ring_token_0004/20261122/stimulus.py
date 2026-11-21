def stimulus(rng, cycles):
    rows = []
    # Phase 1: reset and basic token cycling
    for i in range(8):
        rows.append({'rst': 1 if i < 2 else 0, 'data_in': 0, 'has_data_to_send': 0})
    # Phase 2: token cycling with data send patterns
    patterns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    for i in range(16):
        rows.append({'rst': 0, 'data_in': patterns[i], 'has_data_to_send': 1})
    # Phase 3: alternating has_data_to_send
    for i in range(16):
        rows.append({'rst': 0, 'data_in': (i * 3) & 0xF, 'has_data_to_send': i & 1})
    # Phase 4: reset at various states
    for i in range(12):
        rows.append({'rst': 1 if i % 4 == 3 else 0, 'data_in': i & 0xF, 'has_data_to_send': 1})
    # Phase 5: random exploration
    while len(rows) < cycles:
        r = rng.random()
        if r < 0.05:
            rows.append({'rst': 1, 'data_in': rng.randrange(16), 'has_data_to_send': rng.randrange(2)})
        else:
            rows.append({'rst': 0, 'data_in': rng.randrange(16), 'has_data_to_send': rng.randrange(2)})
    # Trim to exact length
    rows = rows[:cycles]
    # Add mid-cycle changes on some rows for temporal variety
    for i in range(len(rows)):
        if i % 7 == 3 and rows[i]['rst'] == 0:
            rows[i]['mid'] = {'data_in': rng.randrange(16), 'has_data_to_send': rng.randrange(2)}
    return rows

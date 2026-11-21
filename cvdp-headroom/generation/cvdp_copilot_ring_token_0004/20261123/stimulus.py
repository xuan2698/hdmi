def stimulus(rng, cycles):
    rows = []
    # Phase 1: reset and basic token cycling
    for i in range(8):
        rows.append({'rst': 1 if i < 2 else 0, 'data_in': 0, 'has_data_to_send': 0})
    # Phase 2: token cycling with data send toggling
    for i in range(16):
        rows.append({'rst': 0, 'data_in': (i * 3) & 0xF, 'has_data_to_send': i & 1})
    # Phase 3: data patterns while sending
    patterns = [0x0, 0xF, 0x5, 0xA, 0x3, 0xC, 0x1, 0x8, 0x7, 0xE]
    for i in range(20):
        rows.append({'rst': 0, 'data_in': patterns[i % len(patterns)], 'has_data_to_send': 1})
    # Phase 4: idle cycles
    for i in range(8):
        rows.append({'rst': 0, 'data_in': rng.randrange(16), 'has_data_to_send': 0})
    # Phase 5: reset at various states
    for i in range(12):
        r = 1 if i % 4 == 0 else 0
        rows.append({'rst': r, 'data_in': rng.randrange(16), 'has_data_to_send': rng.randrange(2)})
    # Phase 6: mid-cycle changes
    for i in range(12):
        rows.append({'rst': 0, 'data_in': rng.randrange(16), 'has_data_to_send': rng.randrange(2),
                     'mid': {'data_in': rng.randrange(16), 'has_data_to_send': rng.randrange(2)}})
    # Phase 7: consecutive sends
    for i in range(16):
        rows.append({'rst': 0, 'data_in': (i * 7 + 1) & 0xF, 'has_data_to_send': 1})
    # Phase 8: random exploration
    while len(rows) < cycles:
        r = 1 if rng.random() < 0.05 else 0
        row = {'rst': r, 'data_in': rng.randrange(16), 'has_data_to_send': rng.randrange(2)}
        if rng.random() < 0.3:
            row['mid'] = {'data_in': rng.randrange(16), 'has_data_to_send': rng.randrange(2)}
        rows.append(row)
    return rows[:cycles]

def stimulus(rng, cycles):
    rows = []
    # Directed phase: reset, then walk through token states with data patterns
    seq = []
    # Reset pulse
    seq.append({'rst': 1, 'data_in': 0, 'has_data_to_send': 0})
    seq.append({'rst': 1, 'data_in': 15, 'has_data_to_send': 1})
    seq.append({'rst': 0, 'data_in': 0, 'has_data_to_send': 0})
    # Walk token around with has_data_to_send toggling
    for i in range(8):
        seq.append({'rst': 0, 'data_in': (i * 3) & 0xF, 'has_data_to_send': i & 1})
    # Data patterns while sending
    for d in [0, 1, 2, 4, 8, 15, 5, 10, 3, 12]:
        seq.append({'rst': 0, 'data_in': d, 'has_data_to_send': 1})
    # Idle cycles
    for _ in range(6):
        seq.append({'rst': 0, 'data_in': rng.randrange(16), 'has_data_to_send': 0})
    # Mid-cycle changes on some rows
    mid_rows = {5: {'has_data_to_send': 1}, 9: {'data_in': 7}, 14: {'has_data_to_send': 0}}
    # Reset at various states
    for pos in [3, 7, 11]:
        seq.append({'rst': 1, 'data_in': rng.randrange(16), 'has_data_to_send': rng.randrange(2)})
        seq.append({'rst': 0, 'data_in': rng.randrange(16), 'has_data_to_send': rng.randrange(2)})
    # Fill remaining with random exploration
    while len(seq) < cycles:
        r = rng.random()
        if r < 0.05:
            seq.append({'rst': 1, 'data_in': rng.randrange(16), 'has_data_to_send': rng.randrange(2)})
        elif r < 0.15:
            seq.append({'rst': 0, 'data_in': rng.randrange(16), 'has_data_to_send': 0})
        else:
            seq.append({'rst': 0, 'data_in': rng.randrange(16), 'has_data_to_send': rng.randrange(2)})
    seq = seq[:cycles]
    # Build rows with mid dicts
    for i, row in enumerate(seq):
        out = dict(row)
        if i in mid_rows:
            out['mid'] = dict(mid_rows[i])
        rows.append(out)
    return rows

def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        row = {
            'addr_a': rng.randrange(1 << 13),
            'en_a': rng.randrange(2),
            'be_a': rng.randrange(1 << 4),
            'data_in_a': rng.randrange(1 << 32),
            'addr_b': rng.randrange(1 << 13),
            'en_b': rng.randrange(2),
            'be_b': rng.randrange(1 << 4),
            'data_in_b': rng.randrange(1 << 32),
        }
        rows.append(row)
    return rows

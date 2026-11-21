def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        row = {
            'addr_a': rng.randrange(8192),
            'en_a': rng.randrange(2),
            'be_a': rng.randrange(16),
            'data_in_a': rng.randrange(1 << 32),
            'addr_b': rng.randrange(8192),
            'en_b': rng.randrange(2),
            'be_b': rng.randrange(16),
            'data_in_b': rng.randrange(1 << 32),
        }
        if i % 97 == 0:
            row['en_a'] = 0
            row['en_b'] = 0
        if i % 53 == 0:
            row['addr_b'] = row['addr_a']
            row['en_a'] = 1
            row['en_b'] = 1
        if i % 211 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
        if i % 307 == 0:
            row['be_a'] = 0
            row['be_b'] = 0
        rows.append(row)
    return rows

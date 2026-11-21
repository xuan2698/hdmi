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
        if i % 7 == 0:
            row['en_a'] = 1
            row['be_a'] = 15
        if i % 11 == 0:
            row['en_b'] = 1
            row['be_b'] = 15
        if i % 13 == 0:
            row['addr_b'] = row['addr_a']
            row['en_a'] = 1
            row['en_b'] = 1
        if i % 17 == 0:
            row['be_a'] = rng.randrange(16)
            row['be_b'] = rng.randrange(16)
        if i % 23 == 0:
            row['addr_a'] = 0
            row['addr_b'] = 0
            row['en_a'] = 1
            row['en_b'] = 1
            row['be_a'] = 15
            row['be_b'] = 15
        if i % 29 == 0:
            row['en_a'] = 0
            row['en_b'] = 0
        if i % 31 == 0:
            row['be_a'] = 0
            row['be_b'] = 0
        if i % 37 == 0:
            row['addr_a'] = 8191
            row['addr_b'] = 8191
        rows.append(row)
    return rows

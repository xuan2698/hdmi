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
            row['en_a'] = 1
            row['be_a'] = 15
        if i % 89 == 0:
            row['en_b'] = 1
            row['be_b'] = 15
        if i % 53 == 0:
            row['addr_b'] = row['addr_a']
            row['en_b'] = 1
            row['en_a'] = 1
        if i % 211 == 0:
            row['en_a'] = 0
            row['en_b'] = 0
        if i % 37 == 0:
            row['be_a'] = 1 << (i % 4)
            row['be_b'] = 1 << ((i + 2) % 4)
            row['en_a'] = 1
            row['en_b'] = 1
            row['addr_a'] = row['addr_b']
        if i % 71 == 0:
            row['be_a'] = 0
            row['be_b'] = 0
        if i % 131 == 0:
            row['be_a'] = 15
            row['be_b'] = 15
            row['addr_a'] = row['addr_b']
            row['en_a'] = 1
            row['en_b'] = 1
        rows.append(row)
    return rows

def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        if i < 8:
            row = {
                'addr_a': 0, 'en_a': 0, 'be_a': 0, 'data_in_a': 0,
                'addr_b': 0, 'en_b': 0, 'be_b': 0, 'data_in_b': 0,
            }
        elif i < 64:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 15,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 15,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 128:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': rng.randrange(16),
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': rng.randrange(16),
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 256:
            row = {
                'addr_a': rng.randrange(8192), 'en_a': 0, 'be_a': 0, 'data_in_a': 0,
                'addr_b': rng.randrange(8192), 'en_b': 0, 'be_b': 0, 'data_in_b': 0,
            }
        elif i < 512:
            row = {
                'addr_a': rng.randrange(8192), 'en_a': 1,
                'be_a': 1 << rng.randrange(4), 'data_in_a': rng.randrange(1 << 32),
                'addr_b': rng.randrange(8192), 'en_b': 1,
                'be_b': 1 << rng.randrange(4), 'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 1024:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': rng.randrange(16),
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': rng.randrange(16),
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 2048:
            row = {
                'addr_a': rng.randrange(8192), 'en_a': 1, 'be_a': 15,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': rng.randrange(8192), 'en_b': 0, 'be_b': 0, 'data_in_b': 0,
            }
        elif i < 3072:
            row = {
                'addr_a': rng.randrange(8192), 'en_a': 0, 'be_a': 0, 'data_in_a': 0,
                'addr_b': rng.randrange(8192), 'en_b': 1, 'be_b': 15,
                'data_in_b': rng.randrange(1 << 32),
            }
        else:
            row = {
                'addr_a': rng.randrange(8192), 'en_a': rng.randrange(2),
                'be_a': rng.randrange(16), 'data_in_a': rng.randrange(1 << 32),
                'addr_b': rng.randrange(8192), 'en_b': rng.randrange(2),
                'be_b': rng.randrange(16), 'data_in_b': rng.randrange(1 << 32),
            }
        rows.append(row)
    return rows

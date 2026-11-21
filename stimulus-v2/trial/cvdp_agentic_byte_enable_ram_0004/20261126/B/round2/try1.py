def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        if i < 4:
            row = {
                'addr_a': 0,
                'en_a': 0,
                'be_a': 0,
                'data_in_a': 0,
                'addr_b': 0,
                'en_b': 0,
                'be_b': 0,
                'data_in_b': 0,
            }
        elif i < 40:
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
        elif i < 200:
            a = rng.randrange(1 << 13)
            row = {
                'addr_a': a,
                'en_a': 1,
                'be_a': rng.randrange(1 << 4),
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a,
                'en_b': 1,
                'be_b': rng.randrange(1 << 4),
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 400:
            row = {
                'addr_a': rng.randrange(1 << 13),
                'en_a': 1,
                'be_a': 0xF,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': rng.randrange(1 << 13),
                'en_b': 0,
                'be_b': 0,
                'data_in_b': 0,
            }
        elif i < 600:
            row = {
                'addr_a': rng.randrange(1 << 13),
                'en_a': 0,
                'be_a': 0,
                'data_in_a': 0,
                'addr_b': rng.randrange(1 << 13),
                'en_b': 1,
                'be_b': 0xF,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 800:
            row = {
                'addr_a': rng.randrange(1 << 13),
                'en_a': 0,
                'be_a': 0,
                'data_in_a': 0,
                'addr_b': rng.randrange(1 << 13),
                'en_b': 0,
                'be_b': 0,
                'data_in_b': 0,
            }
        elif i < 1000:
            row = {
                'addr_a': rng.randrange(1 << 13),
                'en_a': 1,
                'be_a': rng.randrange(1 << 4),
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': rng.randrange(1 << 13),
                'en_b': 1,
                'be_b': rng.randrange(1 << 4),
                'data_in_b': rng.randrange(1 << 32),
            }
        else:
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

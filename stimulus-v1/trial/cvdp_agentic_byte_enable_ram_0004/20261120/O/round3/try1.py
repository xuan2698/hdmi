def stimulus(rng, cycles):
    rows = []
    for _ in range(4):
        rows.append({'addr_a': 0, 'en_a': 0, 'be_a': 0, 'data_in_a': 0,
                     'addr_b': 0, 'en_b': 0, 'be_b': 0, 'data_in_b': 0})
    hot = [rng.randrange(0, 8192) for _ in range(8)]
    for i in range(200):
        a = hot[i % len(hot)] if i % 3 == 0 else rng.randrange(0, 8192)
        b = hot[(i + 1) % len(hot)] if i % 4 == 0 else rng.randrange(0, 8192)
        rows.append({'addr_a': a, 'en_a': 0, 'be_a': 0, 'data_in_a': 0,
                     'addr_b': b, 'en_b': 1, 'be_b': rng.randrange(1, 16),
                     'data_in_b': rng.randrange(0, 1 << 32)})
    while len(rows) < cycles - 4:
        r = rng.random()
        a = hot[rng.randrange(0, len(hot))] if rng.random() < 0.3 else rng.randrange(0, 8192)
        b = hot[rng.randrange(0, len(hot))] if rng.random() < 0.3 else rng.randrange(0, 8192)
        if r < 0.15:
            b = a
            en_a = 1; en_b = 1
            be_a = rng.randrange(1, 16); be_b = rng.randrange(1, 16)
        elif r < 0.35:
            en_a = 1; en_b = 0
            be_a = rng.randrange(1, 16); be_b = 0
        elif r < 0.55:
            en_a = 0; en_b = 1
            be_a = 0; be_b = rng.randrange(1, 16)
        elif r < 0.75:
            en_a = 1; en_b = 1
            be_a = rng.randrange(1, 16); be_b = rng.randrange(1, 16)
        elif r < 0.9:
            en_a = 0; en_b = 0
            be_a = 0; be_b = 0
        else:
            en_a = 1; en_b = 1
            be_a = 15; be_b = 15
        row = {'addr_a': a, 'en_a': en_a, 'be_a': be_a,
               'data_in_a': rng.randrange(0, 1 << 32),
               'addr_b': b, 'en_b': en_b, 'be_b': be_b,
               'data_in_b': rng.randrange(0, 1 << 32)}
        if rng.random() < 0.1:
            row['mid'] = {'en_a': rng.randrange(0, 2), 'en_b': rng.randrange(0, 2),
                          'be_a': rng.randrange(0, 16), 'be_b': rng.randrange(0, 16)}
        rows.append(row)
    while len(rows) < cycles:
        rows.append({'addr_a': rng.randrange(0, 8192), 'en_a': 0, 'be_a': 0, 'data_in_a': 0,
                     'addr_b': rng.randrange(0, 8192), 'en_b': 0, 'be_b': 0, 'data_in_b': 0})
    return rows[:cycles]

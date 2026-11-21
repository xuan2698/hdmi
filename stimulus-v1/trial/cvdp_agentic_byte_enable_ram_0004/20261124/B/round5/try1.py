def stimulus(rng, cycles):
    rows = []
    for _ in range(6):
        rows.append({'addr_a': 0, 'en_a': 0, 'be_a': 0, 'data_in_a': 0,
                     'addr_b': 0, 'en_b': 0, 'be_b': 0, 'data_in_b': 0})
    hot = [rng.randrange(0, 8192) for _ in range(24)]
    base = rng.randrange(0, 8192)
    for i in range(120):
        a = (base + i) % 8192
        rows.append({'addr_a': a, 'en_a': 1, 'be_a': 0xF,
                     'data_in_a': rng.getrandbits(32),
                     'addr_b': 0, 'en_b': 0, 'be_b': 0, 'data_in_b': 0})
    for i in range(120):
        a = (base + i) % 8192
        rows.append({'addr_a': a, 'en_a': 1,
                     'be_a': rng.choice([0xF, 0x3, 0xC, 0x1, 0x8, 0x5, 0xA, 0x9, 0x6, 0x2, 0x4]),
                     'data_in_a': rng.getrandbits(32),
                     'addr_b': a, 'en_b': 0, 'be_b': 0, 'data_in_b': 0})
    for i in range(300):
        a = rng.choice(hot)
        rows.append({'addr_a': a, 'en_a': 1, 'be_a': rng.getrandbits(4),
                     'data_in_a': rng.getrandbits(32),
                     'addr_b': a, 'en_b': 1, 'be_b': rng.getrandbits(4),
                     'data_in_b': rng.getrandbits(32)})
    for i in range(120):
        a = rng.choice(hot)
        rows.append({'addr_a': a, 'en_a': 1, 'be_a': 0,
                     'data_in_a': rng.getrandbits(32),
                     'addr_b': a, 'en_b': 1, 'be_b': rng.getrandbits(4),
                     'data_in_b': rng.getrandbits(32)})
    for i in range(120):
        a = rng.choice(hot)
        rows.append({'addr_a': a, 'en_a': 1, 'be_a': rng.getrandbits(4),
                     'data_in_a': rng.getrandbits(32),
                     'addr_b': a, 'en_b': 1, 'be_b': 0,
                     'data_in_b': rng.getrandbits(32)})
    for i in range(80):
        a = rng.choice(hot)
        rows.append({'addr_a': a, 'en_a': 1, 'be_a': 0xF,
                     'data_in_a': rng.getrandbits(32),
                     'addr_b': a, 'en_b': 1, 'be_b': 0xF,
                     'data_in_b': rng.getrandbits(32)})
    while len(rows) < 4000:
        r = rng.random()
        if r < 0.12:
            for _ in range(rng.randrange(4, 18)):
                if len(rows) >= 4000:
                    break
                a = rng.choice(hot)
                rows.append({'addr_a': a, 'en_a': 1, 'be_a': rng.getrandbits(4),
                             'data_in_a': rng.getrandbits(32),
                             'addr_b': rng.choice(hot), 'en_b': 0, 'be_b': 0,
                             'data_in_b': 0})
        elif r < 0.24:
            for _ in range(rng.randrange(4, 18)):
                if len(rows) >= 4000:
                    break
                b = rng.choice(hot)
                rows.append({'addr_a': rng.choice(hot), 'en_a': 0, 'be_a': 0,
                             'data_in_a': 0,
                             'addr_b': b, 'en_b': 1, 'be_b': rng.getrandbits(4),
                             'data_in_b': rng.getrandbits(32)})
        elif r < 0.36:
            for _ in range(rng.randrange(2, 10)):
                if len(rows) >= 4000:
                    break
                rows.append({'addr_a': rng.randrange(0, 8192), 'en_a': 0,
                             'be_a': 0, 'data_in_a': 0,
                             'addr_b': rng.randrange(0, 8192), 'en_b': 0,
                             'be_b': 0, 'data_in_b': 0})
        elif r < 0.52:
            a = rng.choice(hot)
            for _ in range(rng.randrange(3, 12)):
                if len(rows) >= 4000:
                    break
                rows.append({'addr_a': a, 'en_a': 1, 'be_a': rng.getrandbits(4),
                             'data_in_a': rng.getrandbits(32),
                             'addr_b': a, 'en_b': 1, 'be_b': rng.getrandbits(4),
                             'data_in_b': rng.getrandbits(32)})
        elif r < 0.64:
            a = rng.choice(hot)
            for _ in range(rng.randrange(3, 9)):
                if len(rows) >= 4000:
                    break
                rows.append({'addr_a': a, 'en_a': 1, 'be_a': 0,
                             'data_in_a': rng.getrandbits(32),
                             'addr_b': a, 'en_b': 1, 'be_b': rng.getrandbits(4),
                             'data_in_b': rng.getrandbits(32)})
        else:
            a = rng.randrange(0, 8192)
            b = rng.randrange(0, 8192)
            if rng.random() < 0.4:
                b = a
            rows.append({'addr_a': a, 'en_a': rng.getrandbits(1),
                         'be_a': rng.getrandbits(4),
                         'data_in_a': rng.getrandbits(32),
                         'addr_b': b, 'en_b': rng.getrandbits(1),
                         'be_b': rng.getrandbits(4),
                         'data_in_b': rng.getrandbits(32)})
    return rows[:4000]

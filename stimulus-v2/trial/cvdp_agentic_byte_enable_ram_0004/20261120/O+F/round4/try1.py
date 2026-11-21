def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        addr_a = rng.randrange(8192)
        en_a = 1 if rng.random() < 0.5 else 0
        be_a = rng.randrange(16)
        data_in_a = rng.randrange(1 << 32)
        addr_b = rng.randrange(8192)
        en_b = 1 if rng.random() < 0.5 else 0
        be_b = rng.randrange(16)
        data_in_b = rng.randrange(1 << 32)
        if i % 97 == 0:
            addr_a = 0
            addr_b = 0
            en_a = 1
            en_b = 1
            be_a = 15
            be_b = 15
        if i % 53 == 0:
            addr_b = addr_a
            en_b = 1
            be_b = rng.randrange(16)
        if i % 31 == 0:
            be_b = 4
        if i % 17 == 0:
            be_b = 4
            en_b = 1
            addr_b = addr_a
        if i % 11 == 0:
            be_b = 4
            en_b = 1
        if i % 7 == 0:
            be_b = 4
        rows.append({
            'addr_a': addr_a,
            'en_a': en_a,
            'be_a': be_a,
            'data_in_a': data_in_a,
            'addr_b': addr_b,
            'en_b': en_b,
            'be_b': be_b,
            'data_in_b': data_in_b,
        })
    return rows

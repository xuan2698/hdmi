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
        if i % 131 == 0:
            addr_a = rng.randrange(8192)
            addr_b = addr_a
            en_a = 1
            en_b = 1
            be_a = rng.randrange(16)
            be_b = rng.randrange(16)
        if i % 53 == 0:
            be_a = 0
            be_b = 0
        if i % 211 == 0:
            be_a = 1 << rng.randrange(4)
            be_b = 1 << rng.randrange(4)
        if i % 307 == 0:
            addr_a = rng.randrange(8192)
            addr_b = addr_a
            en_a = 1
            en_b = 1
            be_a = 15
            be_b = 0
        if i % 401 == 0:
            addr_a = rng.randrange(8192)
            addr_b = addr_a
            en_a = 1
            en_b = 1
            be_a = 0
            be_b = 15
        if i % 509 == 0:
            en_a = 0
            en_b = 0
            be_a = 0
            be_b = 0
        if i % 613 == 0:
            addr_a = rng.randrange(8192)
            addr_b = addr_a
            en_a = 1
            en_b = 1
            be_a = 15
            be_b = 15
            data_in_a = rng.randrange(1 << 32)
            data_in_b = rng.randrange(1 << 32)
        if i % 719 == 0:
            addr_a = rng.randrange(8192)
            addr_b = addr_a
            en_a = 1
            en_b = 1
            be_a = 1 << rng.randrange(4)
            be_b = 1 << rng.randrange(4)
        if i % 827 == 0:
            addr_a = rng.randrange(8192)
            addr_b = addr_a
            en_a = 1
            en_b = 1
            be_a = 15
            be_b = rng.randrange(16)
        if i % 929 == 0:
            addr_a = rng.randrange(8192)
            addr_b = addr_a
            en_a = 1
            en_b = 1
            be_a = rng.randrange(16)
            be_b = 15
        if i % 1031 == 0:
            addr_a = rng.randrange(8192)
            addr_b = addr_a
            en_a = 1
            en_b = 1
            be_a = 0
            be_b = 0
        if i % 1153 == 0:
            addr_a = rng.randrange(8192)
            addr_b = addr_a
            en_a = 0
            en_b = 1
            be_a = 15
            be_b = 15
        if i % 1277 == 0:
            addr_a = rng.randrange(8192)
            addr_b = addr_a
            en_a = 1
            en_b = 0
            be_a = 15
            be_b = 15
        if i % 1409 == 0:
            addr_a = rng.randrange(8192)
            addr_b = addr_a
            en_a = 0
            en_b = 0
            be_a = 15
            be_b = 15
        rows.append({
            'addr_a': addr_a & 0x1FFF,
            'en_a': en_a & 1,
            'be_a': be_a & 0xF,
            'data_in_a': data_in_a & 0xFFFFFFFF,
            'addr_b': addr_b & 0x1FFF,
            'en_b': en_b & 1,
            'be_b': be_b & 0xF,
            'data_in_b': data_in_b & 0xFFFFFFFF,
        })
    return rows

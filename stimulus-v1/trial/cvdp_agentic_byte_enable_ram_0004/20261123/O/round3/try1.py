def stimulus(rng, cycles):
    rows = []
    addr_a = 0
    addr_b = 0
    en_a = 0
    en_b = 0
    be_a = 0
    be_b = 0
    data_in_a = 0
    data_in_b = 0
    for i in range(cycles):
        if i < 4:
            en_a = 0
            en_b = 0
            be_a = 0
            be_b = 0
            data_in_a = 0
            data_in_b = 0
            addr_a = 0
            addr_b = 0
        else:
            if i % 37 == 0:
                addr_a = rng.randrange(0, 8192)
                addr_b = rng.randrange(0, 8192)
            if i % 53 == 0:
                en_a = rng.randrange(0, 2)
                en_b = rng.randrange(0, 2)
            if i % 41 == 0:
                be_a = rng.randrange(0, 16)
                be_b = rng.randrange(0, 16)
            if i % 29 == 0:
                data_in_a = rng.randrange(0, 2**32)
                data_in_b = rng.randrange(0, 2**32)
            if i % 97 == 0:
                addr_b = addr_a
                en_a = 1
                en_b = 1
                be_a = rng.randrange(0, 16)
                be_b = rng.randrange(0, 16)
            if i % 71 == 0:
                en_a = 0
                en_b = 0
                be_a = 0
                be_b = 0
            if i % 61 == 0:
                en_a = 1
                en_b = 1
                be_a = 15
                be_b = 15
            if i % 13 == 0:
                addr_a = (addr_a + 1) % 8192
            if i % 17 == 0:
                addr_b = (addr_b + 1) % 8192
        row = {
            'addr_a': addr_a & 0x1FFF,
            'en_a': en_a & 1,
            'be_a': be_a & 0xF,
            'data_in_a': data_in_a & 0xFFFFFFFF,
            'addr_b': addr_b & 0x1FFF,
            'en_b': en_b & 1,
            'be_b': be_b & 0xF,
            'data_in_b': data_in_b & 0xFFFFFFFF,
        }
        rows.append(row)
    return rows

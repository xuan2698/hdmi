def stimulus(rng, cycles):
    rows = []
    addr_a = 0
    addr_b = 0
    data_in_a = 0
    data_in_b = 0
    be_a = 0
    be_b = 0
    en_a = 0
    en_b = 0
    hot_a = 0
    hot_b = 0
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
        elif i < 10:
            en_a = 1
            en_b = 0
            be_a = 0xF
            be_b = 0
            addr_a = (i - 4) & 0x1FFF
            data_in_a = ((i * 0x11111111) ^ 0xA5A5A5A5) & 0xFFFFFFFF
            data_in_b = 0
        elif i < 16:
            en_a = 0
            en_b = 1
            be_a = 0
            be_b = 0xF
            addr_b = (i - 10) & 0x1FFF
            data_in_b = ((i * 0x22222222) ^ 0x5A5A5A5A) & 0xFFFFFFFF
            data_in_a = 0
        elif i < 22:
            en_a = 1
            en_b = 1
            be_a = 0xF
            be_b = 0xF
            addr_a = (i - 16) & 0x1FFF
            addr_b = addr_a
            data_in_a = (0xDEADBEEF ^ (i << 4)) & 0xFFFFFFFF
            data_in_b = (0xCAFEBABE ^ (i << 8)) & 0xFFFFFFFF
        else:
            mode = rng.randrange(100)
            if mode < 15:
                en_a = 0
                en_b = 0
                be_a = 0
                be_b = 0
                data_in_a = 0
                data_in_b = 0
            elif mode < 35:
                en_a = 1
                en_b = 0
                be_a = rng.randrange(1, 16)
                be_b = 0
                addr_a = rng.randrange(8192)
                data_in_a = rng.randrange(1 << 32)
                data_in_b = 0
            elif mode < 55:
                en_a = 0
                en_b = 1
                be_a = 0
                be_b = rng.randrange(1, 16)
                addr_b = rng.randrange(8192)
                data_in_b = rng.randrange(1 << 32)
                data_in_a = 0
            elif mode < 75:
                en_a = 1
                en_b = 1
                be_a = rng.randrange(1, 16)
                be_b = rng.randrange(1, 16)
                addr_a = rng.randrange(8192)
                addr_b = rng.randrange(8192)
                if addr_a == addr_b:
                    addr_b = (addr_b + 1) & 0x1FFF
                data_in_a = rng.randrange(1 << 32)
                data_in_b = rng.randrange(1 << 32)
            elif mode < 90:
                en_a = 1
                en_b = 1
                be_a = rng.randrange(1, 16)
                be_b = rng.randrange(1, 16)
                addr_a = rng.randrange(8192)
                addr_b = addr_a
                data_in_a = rng.randrange(1 << 32)
                data_in_b = rng.randrange(1 << 32)
            else:
                if rng.randrange(2):
                    hot_a = rng.randrange(8192)
                    hot_b = hot_a
                en_a = 1
                en_b = 1
                be_a = rng.randrange(1, 16)
                be_b = rng.randrange(1, 16)
                addr_a = hot_a
                addr_b = hot_b
                data_in_a = rng.randrange(1 << 32)
                data_in_b = rng.randrange(1 << 32)
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

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
    for i in range(cycles):
        if i < 4:
            addr_a = 0
            addr_b = 0
            en_a = 0
            en_b = 0
            be_a = 0
            be_b = 0
            data_in_a = 0
            data_in_b = 0
        else:
            phase = (i // 96) % 7
            if phase == 0:
                if i % 6 == 0:
                    addr_a = rng.randrange(0, 8192)
                    addr_b = addr_a
                en_a = 1
                en_b = 1
                be_a = rng.choice([0xF, 0x3, 0xC, 0x5, 0xA, 0x1, 0xE, 0x7])
                be_b = rng.choice([0xF, 0x3, 0xC, 0x5, 0xA, 0x2, 0xD, 0x9])
                data_in_a = rng.randrange(0, 1 << 32)
                data_in_b = rng.randrange(0, 1 << 32)
            elif phase == 1:
                if i % 32 == 0:
                    addr_a = rng.randrange(0, 8192)
                en_a = 0
                be_a = 0
                data_in_a = 0
                if rng.random() < 0.7:
                    addr_b = rng.randrange(0, 8192)
                en_b = 1
                be_b = rng.choice([0xF, 0x1, 0x2, 0x4, 0x8, 0x3, 0xC, 0x6])
                data_in_b = rng.randrange(0, 1 << 32)
            elif phase == 2:
                addr_a = rng.randrange(0, 8192)
                addr_b = rng.randrange(0, 8192)
                en_a = 1
                en_b = 1
                be_a = 0xF
                be_b = 0xF
                data_in_a = rng.randrange(0, 1 << 32)
                data_in_b = rng.randrange(0, 1 << 32)
            elif phase == 3:
                if i % 40 == 0:
                    addr_a = rng.randrange(0, 8192)
                    addr_b = rng.randrange(0, 8192)
                en_a = 0
                en_b = 0
                be_a = 0
                be_b = 0
                data_in_a = 0
                data_in_b = 0
            elif phase == 4:
                if rng.random() < 0.5:
                    addr_a = rng.randrange(0, 8192)
                if rng.random() < 0.5:
                    addr_b = rng.randrange(0, 8192)
                if rng.random() < 0.35:
                    addr_b = addr_a
                en_a = 1 if rng.random() < 0.75 else 0
                en_b = 1 if rng.random() < 0.75 else 0
                be_a = rng.randrange(0, 16)
                be_b = rng.randrange(0, 16)
                data_in_a = rng.randrange(0, 1 << 32)
                data_in_b = rng.randrange(0, 1 << 32)
            elif phase == 5:
                if i % 2 == 0:
                    addr_a = rng.randrange(0, 8192)
                    en_a = 1
                    en_b = 0
                    be_a = rng.choice([0xF, 0x3, 0xC, 0x1])
                    data_in_a = rng.randrange(0, 1 << 32)
                    be_b = 0
                    data_in_b = 0
                else:
                    addr_b = rng.randrange(0, 8192)
                    en_b = 1
                    en_a = 0
                    be_b = rng.choice([0xF, 0x5, 0xA, 0x8])
                    data_in_b = rng.randrange(0, 1 << 32)
                    be_a = 0
                    data_in_a = 0
            else:
                if i % 16 == 0:
                    addr_a = rng.randrange(0, 8192)
                    addr_b = rng.randrange(0, 8192)
                en_a = 1 if rng.random() < 0.4 else 0
                en_b = 1 if rng.random() < 0.4 else 0
                be_a = rng.randrange(0, 16)
                be_b = rng.randrange(0, 16)
                data_in_a = rng.randrange(0, 1 << 32)
                data_in_b = rng.randrange(0, 1 << 32)
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
        if i >= 4 and rng.random() < 0.18:
            mid = {}
            if rng.random() < 0.5:
                mid['en_a'] = 1 - en_a
            if rng.random() < 0.5:
                mid['en_b'] = 1 - en_b
            if rng.random() < 0.35:
                mid['be_a'] = rng.randrange(0, 16)
            if rng.random() < 0.35:
                mid['be_b'] = rng.randrange(0, 16)
            if rng.random() < 0.3:
                mid['data_in_a'] = rng.randrange(0, 1 << 32)
            if rng.random() < 0.3:
                mid['data_in_b'] = rng.randrange(0, 1 << 32)
            if rng.random() < 0.2:
                mid['addr_a'] = rng.randrange(0, 8192)
            if rng.random() < 0.2:
                mid['addr_b'] = rng.randrange(0, 8192)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows

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
            addr_a = 0
            addr_b = 0
            en_a = 0
            en_b = 0
            be_a = 0
            be_b = 0
            data_in_a = 0
            data_in_b = 0
        else:
            phase = i % 200
            if phase < 6:
                en_a = 0
                en_b = 0
                be_a = 0
                be_b = 0
            elif phase < 30:
                addr_a = (addr_a + 1) & 0x1FFF
                addr_b = addr_a
                en_a = 1
                en_b = 1
                be_a = rng.randrange(0, 16)
                be_b = rng.randrange(0, 16)
                data_in_a = rng.randrange(0, 1 << 32)
                data_in_b = rng.randrange(0, 1 << 32)
            elif phase < 50:
                addr_a = rng.randrange(0, 8192)
                addr_b = addr_a
                en_a = 1
                en_b = 1
                be_a = 0
                be_b = rng.randrange(1, 16)
                data_in_a = rng.randrange(0, 1 << 32)
                data_in_b = rng.randrange(0, 1 << 32)
            elif phase < 70:
                addr_a = rng.randrange(0, 8192)
                addr_b = addr_a
                en_a = 1
                en_b = 1
                be_a = rng.randrange(1, 16)
                be_b = 0
                data_in_a = rng.randrange(0, 1 << 32)
                data_in_b = rng.randrange(0, 1 << 32)
            elif phase < 90:
                addr_a = rng.randrange(0, 8192)
                addr_b = rng.randrange(0, 8192)
                en_a = 1
                en_b = 1
                be_a = rng.randrange(0, 16)
                be_b = rng.randrange(0, 16)
                data_in_a = rng.randrange(0, 1 << 32)
                data_in_b = rng.randrange(0, 1 << 32)
            elif phase < 110:
                addr_a = rng.randrange(0, 8192)
                addr_b = addr_a if rng.random() < 0.5 else rng.randrange(0, 8192)
                en_a = 1
                en_b = 1 if rng.random() < 0.6 else 0
                be_a = 1 << rng.randrange(0, 4)
                be_b = 1 << rng.randrange(0, 4)
                data_in_a = rng.randrange(0, 1 << 32)
                data_in_b = rng.randrange(0, 1 << 32)
            elif phase < 130:
                addr_a = rng.randrange(0, 8192)
                addr_b = rng.randrange(0, 8192)
                en_a = 0
                en_b = 0
                be_a = 0
                be_b = 0
            else:
                if rng.random() < 0.6:
                    addr_a = rng.randrange(0, 8192)
                if rng.random() < 0.6:
                    addr_b = rng.randrange(0, 8192)
                if rng.random() < 0.3:
                    addr_b = addr_a
                r = rng.random()
                if r < 0.3:
                    en_a, en_b = 1, 1
                elif r < 0.55:
                    en_a, en_b = 1, 0
                elif r < 0.8:
                    en_a, en_b = 0, 1
                else:
                    en_a, en_b = 0, 0
                br = rng.random()
                if br < 0.35:
                    be_a = 15
                elif br < 0.7:
                    be_a = rng.randrange(0, 16)
                else:
                    be_a = 0
                br = rng.random()
                if br < 0.35:
                    be_b = 15
                elif br < 0.7:
                    be_b = rng.randrange(0, 16)
                else:
                    be_b = 0
                dr = rng.random()
                if dr < 0.25:
                    data_in_a = 0
                elif dr < 0.45:
                    data_in_a = 0xFFFFFFFF
                elif dr < 0.65:
                    data_in_a = rng.randrange(0, 1 << 32)
                else:
                    data_in_a = (rng.randrange(0, 256) * 0x01010101) & 0xFFFFFFFF
                dr = rng.random()
                if dr < 0.25:
                    data_in_b = 0
                elif dr < 0.45:
                    data_in_b = 0xFFFFFFFF
                elif dr < 0.65:
                    data_in_b = rng.randrange(0, 1 << 32)
                else:
                    data_in_b = (rng.randrange(0, 256) * 0x01010101) & 0xFFFFFFFF
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
            if rng.random() < 0.3:
                mid['be_a'] = rng.randrange(0, 16)
            if rng.random() < 0.3:
                mid['be_b'] = rng.randrange(0, 16)
            if rng.random() < 0.3:
                mid['data_in_a'] = rng.randrange(0, 1 << 32)
            if rng.random() < 0.3:
                mid['data_in_b'] = rng.randrange(0, 1 << 32)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows

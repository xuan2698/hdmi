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
        if i < 3:
            addr_a = 0
            addr_b = 0
            en_a = 0
            en_b = 0
            be_a = 0
            be_b = 0
            data_in_a = 0
            data_in_b = 0
        else:
            phase = (i // 64) % 6
            if phase == 0:
                # Directed collision: same address, both enabled, mixed byte enables
                if i % 8 == 0:
                    addr_a = rng.randrange(0, 8192)
                    addr_b = addr_a
                en_a = 1
                en_b = 1
                be_a = rng.choice([0xF, 0x3, 0xC, 0x5, 0xA, 0x1, 0xE])
                be_b = rng.choice([0xF, 0x3, 0xC, 0x5, 0xA, 0x2, 0xD])
                data_in_a = rng.randrange(0, 1 << 32)
                data_in_b = rng.randrange(0, 1 << 32)
            elif phase == 1:
                # Long stable read run on port A, writes on B
                if i % 40 == 0:
                    addr_a = rng.randrange(0, 8192)
                en_a = 0
                be_a = 0
                data_in_a = 0
                if rng.random() < 0.6:
                    addr_b = rng.randrange(0, 8192)
                en_b = 1
                be_b = rng.choice([0xF, 0x1, 0x2, 0x4, 0x8, 0x3, 0xC])
                data_in_b = rng.randrange(0, 1 << 32)
            elif phase == 2:
                # Full writes both ports, random addresses
                addr_a = rng.randrange(0, 8192)
                addr_b = rng.randrange(0, 8192)
                en_a = 1
                en_b = 1
                be_a = 0xF
                be_b = 0xF
                data_in_a = rng.randrange(0, 1 << 32)
                data_in_b = rng.randrange(0, 1 << 32)
            elif phase == 3:
                # Idle / read-only, hold addresses
                if i % 50 == 0:
                    addr_a = rng.randrange(0, 8192)
                    addr_b = rng.randrange(0, 8192)
                en_a = 0
                en_b = 0
                be_a = 0
                be_b = 0
                data_in_a = 0
                data_in_b = 0
            elif phase == 4:
                # Partial byte writes, occasional same address
                if rng.random() < 0.5:
                    addr_a = rng.randrange(0, 8192)
                if rng.random() < 0.5:
                    addr_b = rng.randrange(0, 8192)
                if rng.random() < 0.3:
                    addr_b = addr_a
                en_a = 1 if rng.random() < 0.7 else 0
                en_b = 1 if rng.random() < 0.7 else 0
                be_a = rng.randrange(0, 16)
                be_b = rng.randrange(0, 16)
                data_in_a = rng.randrange(0, 1 << 32)
                data_in_b = rng.randrange(0, 1 << 32)
            else:
                # Alternating single-port writes
                if i % 2 == 0:
                    addr_a = rng.randrange(0, 8192)
                    en_a = 1
                    en_b = 0
                    be_a = rng.choice([0xF, 0x3, 0xC])
                    data_in_a = rng.randrange(0, 1 << 32)
                    be_b = 0
                    data_in_b = 0
                else:
                    addr_b = rng.randrange(0, 8192)
                    en_b = 1
                    en_a = 0
                    be_b = rng.choice([0xF, 0x5, 0xA])
                    data_in_b = rng.randrange(0, 1 << 32)
                    be_a = 0
                    data_in_a = 0
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
        if i >= 3 and rng.random() < 0.15:
            mid = {}
            if rng.random() < 0.5:
                mid['en_a'] = 1 - en_a
            if rng.random() < 0.5:
                mid['en_b'] = 1 - en_b
            if rng.random() < 0.3:
                mid['be_a'] = rng.randrange(0, 16)
            if rng.random() < 0.3:
                mid['be_b'] = rng.randrange(0, 16)
            if rng.random() < 0.25:
                mid['data_in_a'] = rng.randrange(0, 1 << 32)
            if rng.random() < 0.25:
                mid['data_in_b'] = rng.randrange(0, 1 << 32)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows

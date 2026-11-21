def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        if i < 8:
            row = {'addr_a': 0, 'en_a': 0, 'be_a': 0, 'data_in_a': 0,
                   'addr_b': 0, 'en_b': 0, 'be_b': 0, 'data_in_b': 0}
        elif i < 16:
            row = {'addr_a': i & 0x1FFF, 'en_a': 1, 'be_a': 0xF,
                   'data_in_a': (i * 0x01010101) & 0xFFFFFFFF,
                   'addr_b': (i + 1) & 0x1FFF, 'en_b': 1, 'be_b': 0xF,
                   'data_in_b': (i * 0x02020202) & 0xFFFFFFFF}
        elif i < 24:
            a = (i * 7) & 0x1FFF
            row = {'addr_a': a, 'en_a': 1, 'be_a': rng.randrange(16),
                   'data_in_a': rng.randrange(1 << 32),
                   'addr_b': a, 'en_b': 1, 'be_b': rng.randrange(16),
                   'data_in_b': rng.randrange(1 << 32)}
        elif i < 32:
            row = {'addr_a': rng.randrange(8192), 'en_a': 1, 'be_a': 0,
                   'data_in_a': rng.randrange(1 << 32),
                   'addr_b': rng.randrange(8192), 'en_b': 1, 'be_b': 0,
                   'data_in_b': rng.randrange(1 << 32)}
        elif i < 40:
            row = {'addr_a': rng.randrange(8192), 'en_a': 0, 'be_a': 0xF,
                   'data_in_a': rng.randrange(1 << 32),
                   'addr_b': rng.randrange(8192), 'en_b': 0, 'be_b': 0xF,
                   'data_in_b': rng.randrange(1 << 32)}
        elif i < 48:
            a = rng.randrange(8192)
            row = {'addr_a': a, 'en_a': 1, 'be_a': 0xF,
                   'data_in_a': rng.randrange(1 << 32),
                   'addr_b': a, 'en_b': 1, 'be_b': 0xF,
                   'data_in_b': rng.randrange(1 << 32)}
        elif i < 56:
            a = rng.randrange(8192)
            row = {'addr_a': a, 'en_a': 1, 'be_a': 0x5,
                   'data_in_a': rng.randrange(1 << 32),
                   'addr_b': a, 'en_b': 1, 'be_b': 0xA,
                   'data_in_b': rng.randrange(1 << 32)}
        elif i < 64:
            a = rng.randrange(8192)
            row = {'addr_a': a, 'en_a': 1, 'be_a': 0x0,
                   'data_in_a': rng.randrange(1 << 32),
                   'addr_b': a, 'en_b': 1, 'be_b': 0xF,
                   'data_in_b': rng.randrange(1 << 32)}
        elif i < 72:
            a = rng.randrange(8192)
            row = {'addr_a': a, 'en_a': 1, 'be_a': 0xF,
                   'data_in_a': rng.randrange(1 << 32),
                   'addr_b': a, 'en_b': 1, 'be_b': 0x0,
                   'data_in_b': rng.randrange(1 << 32)}
        elif i < 80:
            a = rng.randrange(8192)
            row = {'addr_a': a, 'en_a': 0, 'be_a': 0xF,
                   'data_in_a': rng.randrange(1 << 32),
                   'addr_b': a, 'en_b': 1, 'be_b': 0xF,
                   'data_in_b': rng.randrange(1 << 32)}
        elif i < 88:
            a = rng.randrange(8192)
            row = {'addr_a': a, 'en_a': 1, 'be_a': 0xF,
                   'data_in_a': rng.randrange(1 << 32),
                   'addr_b': a, 'en_b': 0, 'be_b': 0xF,
                   'data_in_b': rng.randrange(1 << 32)}
        elif i < 96:
            a = rng.randrange(8192)
            row = {'addr_a': a, 'en_a': 1, 'be_a': 0x1,
                   'data_in_a': rng.randrange(1 << 32),
                   'addr_b': a, 'en_b': 1, 'be_b': 0xE,
                   'data_in_b': rng.randrange(1 << 32)}
        elif i < 104:
            a = rng.randrange(8192)
            row = {'addr_a': a, 'en_a': 1, 'be_a': 0xE,
                   'data_in_a': rng.randrange(1 << 32),
                   'addr_b': a, 'en_b': 1, 'be_b': 0x1,
                   'data_in_b': rng.randrange(1 << 32)}
        elif i < 112:
            a = rng.randrange(8192)
            row = {'addr_a': a, 'en_a': 1, 'be_a': 0x3,
                   'data_in_a': rng.randrange(1 << 32),
                   'addr_b': a, 'en_b': 1, 'be_b': 0xC,
                   'data_in_b': rng.randrange(1 << 32)}
        elif i < 120:
            a = rng.randrange(8192)
            row = {'addr_a': a, 'en_a': 1, 'be_a': 0xC,
                   'data_in_a': rng.randrange(1 << 32),
                   'addr_b': a, 'en_b': 1, 'be_b': 0x3,
                   'data_in_b': rng.randrange(1 << 32)}
        elif i < 128:
            a = rng.randrange(8192)
            row = {'addr_a': a, 'en_a': 1, 'be_a': 0x2,
                   'data_in_a': rng.randrange(1 << 32),
                   'addr_b': a, 'en_b': 1, 'be_b': 0x4,
                   'data_in_b': rng.randrange(1 << 32)}
        elif i < 136:
            a = rng.randrange(8192)
            row = {'addr_a': a, 'en_a': 1, 'be_a': 0x4,
                   'data_in_a': rng.randrange(1 << 32),
                   'addr_b': a, 'en_b': 1, 'be_b': 0x2,
                   'data_in_b': rng.randrange(1 << 32)}
        elif i < 144:
            a = rng.randrange(8192)
            row = {'addr_a': a, 'en_a': 1, 'be_a': 0x8,
                   'data_in_a': rng.randrange(1 << 32),
                   'addr_b': a, 'en_b': 1, 'be_b': 0x1,
                   'data_in_b': rng.randrange(1 << 32)}
        elif i < 152:
            a = rng.randrange(8192)
            row = {'addr_a': a, 'en_a': 1, 'be_a': 0x1,
                   'data_in_a': rng.randrange(1 << 32),
                   'addr_b': a, 'en_b': 1, 'be_b': 0x8,
                   'data_in_b': rng.randrange(1 << 32)}
        else:
            row = {'addr_a': rng.randrange(8192), 'en_a': rng.randrange(2),
                   'be_a': rng.randrange(16), 'data_in_a': rng.randrange(1 << 32),
                   'addr_b': rng.randrange(8192), 'en_b': rng.randrange(2),
                   'be_b': rng.randrange(16), 'data_in_b': rng.randrange(1 << 32)}
        rows.append(row)
    return rows

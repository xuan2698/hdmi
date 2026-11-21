def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        if i < 4:
            row = {
                'addr_a': 0, 'en_a': 0, 'be_a': 0, 'data_in_a': 0,
                'addr_b': 0, 'en_b': 0, 'be_b': 0, 'data_in_b': 0,
            }
        elif i < 8:
            row = {
                'addr_a': rng.randrange(8192), 'en_a': 1, 'be_a': 15,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': rng.randrange(8192), 'en_b': 1, 'be_b': 15,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 12:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': rng.randrange(16),
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': rng.randrange(16),
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 16:
            row = {
                'addr_a': rng.randrange(8192), 'en_a': 0, 'be_a': 0,
                'data_in_a': 0,
                'addr_b': rng.randrange(8192), 'en_b': 0, 'be_b': 0,
                'data_in_b': 0,
            }
        elif i < 24:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 15,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 15,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 32:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 0,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 15,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 40:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 15,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 0,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 48:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 1,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 2,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 56:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 2,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 4,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 64:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 4,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 8,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 72:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 8,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 1,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 80:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 3,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 12,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 88:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 12,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 3,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 96:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 5,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 10,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 104:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 10,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 5,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 112:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 6,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 9,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 120:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 9,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 6,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 128:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 7,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 11,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 136:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 11,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 7,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 144:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 13,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 14,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 152:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 14,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 13,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 160:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 15,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 15,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 168:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 0,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 0,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 176:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 15,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 0, 'be_b': 15,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 184:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 0, 'be_a': 15,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': 15,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 192:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 15,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': (a + 1) % 8192, 'en_b': 1, 'be_b': 15,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 200:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 15,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': (a + 4096) % 8192, 'en_b': 1, 'be_b': 15,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 208:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 15,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': (a + 8191) % 8192, 'en_b': 1, 'be_b': 15,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 216:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 15,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': (a + 2) % 8192, 'en_b': 1, 'be_b': 15,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 224:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 15,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': (a + 3) % 8192, 'en_b': 1, 'be_b': 15,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 232:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 15,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': (a + 4) % 8192, 'en_b': 1, 'be_b': 15,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 240:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 15,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': (a + 5) % 8192, 'en_b': 1, 'be_b': 15,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 248:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 15,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': (a + 6) % 8192, 'en_b': 1, 'be_b': 15,
                'data_in_b': rng.randrange(1 << 32),
            }
        elif i < 256:
            a = rng.randrange(8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 15,
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': (a + 7) % 8192, 'en_b': 1, 'be_b': 15,
                'data_in_b': rng.randrange(1 << 32),
            }
        else:
            row = {
                'addr_a': rng.randrange(8192),
                'en_a': rng.randrange(2),
                'be_a': rng.randrange(16),
                'data_in_a': rng.randrange(1 << 32),
                'addr_b': rng.randrange(8192),
                'en_b': rng.randrange(2),
                'be_b': rng.randrange(16),
                'data_in_b': rng.randrange(1 << 32),
            }
        rows.append(row)
    return rows

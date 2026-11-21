def stimulus(rng, cycles):
    rows = []
    # Directed phase: exercise collision, byte enables, same/diff addresses
    patterns = [
        # (addr_a, en_a, be_a, data_a, addr_b, en_b, be_b, data_b)
        (0, 1, 0xF, 0xDEADBEEF, 0, 1, 0xF, 0xCAFEBABE),  # collision full
        (0, 1, 0x1, 0x11223344, 0, 1, 0xE, 0x55667788),  # collision partial A wins byte0
        (0, 1, 0x0, 0x00000000, 0, 1, 0xF, 0xAABBCCDD),  # collision A disabled bytes
        (1, 1, 0xF, 0x01020304, 2, 1, 0xF, 0x05060708),  # independent writes
        (1, 0, 0x0, 0x00000000, 2, 0, 0x0, 0x00000000),  # reads
        (1, 0, 0x0, 0x00000000, 2, 0, 0x0, 0x00000000),  # reads pipelined
        (3, 1, 0x3, 0xAAAAAAAA, 3, 1, 0xC, 0xBBBBBBBB),  # collision split bytes
        (3, 0, 0x0, 0x00000000, 3, 0, 0x0, 0x00000000),
        (4, 1, 0x5, 0x12345678, 5, 1, 0xA, 0x9ABCDEF0),
        (4, 0, 0x0, 0x00000000, 5, 0, 0x0, 0x00000000),
        (4, 0, 0x0, 0x00000000, 5, 0, 0x0, 0x00000000),
        (6, 1, 0x0, 0xFFFFFFFF, 6, 1, 0x0, 0x00000000),  # collision no bytes
        (6, 0, 0x0, 0x00000000, 6, 0, 0x0, 0x00000000),
        (7, 1, 0xF, 0xFFFFFFFF, 7, 1, 0xF, 0x00000000),  # collision A wins all
        (7, 0, 0x0, 0x00000000, 7, 0, 0x0, 0x00000000),
        (8, 1, 0x2, 0x0000FF00, 8, 1, 0x4, 0x00FF0000),  # collision disjoint bytes
        (8, 0, 0x0, 0x00000000, 8, 0, 0x0, 0x00000000),
        (8, 0, 0x0, 0x00000000, 8, 0, 0x0, 0x00000000),
    ]
    for p in patterns:
        rows.append({
            'addr_a': p[0], 'en_a': p[1], 'be_a': p[2], 'data_in_a': p[3],
            'addr_b': p[4], 'en_b': p[5], 'be_b': p[6], 'data_in_b': p[7],
        })
    # Fill remaining with seeded random, biased toward activity
    while len(rows) < cycles:
        r = rng.random()
        if r < 0.15:
            # idle read
            a = rng.randrange(8192)
            b = rng.randrange(8192)
            rows.append({
                'addr_a': a, 'en_a': 0, 'be_a': 0, 'data_in_a': 0,
                'addr_b': b, 'en_b': 0, 'be_b': 0, 'data_in_b': 0,
            })
        elif r < 0.45:
            # collision
            a = rng.randrange(8192)
            rows.append({
                'addr_a': a, 'en_a': 1, 'be_a': rng.randrange(16),
                'data_in_a': rng.getrandbits(32),
                'addr_b': a, 'en_b': 1, 'be_b': rng.randrange(16),
                'data_in_b': rng.getrandbits(32),
            })
        else:
            rows.append({
                'addr_a': rng.randrange(8192), 'en_a': rng.randrange(2),
                'be_a': rng.randrange(16), 'data_in_a': rng.getrandbits(32),
                'addr_b': rng.randrange(8192), 'en_b': rng.randrange(2),
                'be_b': rng.randrange(16), 'data_in_b': rng.getrandbits(32),
            })
    return rows[:cycles]

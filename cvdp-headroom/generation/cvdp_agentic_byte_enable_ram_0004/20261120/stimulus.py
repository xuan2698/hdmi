def stimulus(rng, cycles):
    rows = []
    # Directed corner addresses: 0, 1, 2, 3, 0x1FFF, 0x1FFE, 0x1000, 0x0FFF
    corners = [0, 1, 2, 3, 0x1FFF, 0x1FFE, 0x1000, 0x0FFF, 0x1FFD, 0x0800]
    # Byte-enable patterns
    bes = [0x0, 0x1, 0x2, 0x4, 0x8, 0x3, 0xC, 0xF, 0x5, 0xA, 0x7, 0xE]
    # Data patterns
    datas = [0x00000000, 0xFFFFFFFF, 0xAAAAAAAA, 0x55555555,
             0xDEADBEEF, 0xCAFEBABE, 0x12345678, 0x87654321,
             0x00FF00FF, 0xFF00FF00, 0x0F0F0F0F, 0xF0F0F0F0]

    for i in range(cycles):
        phase = i % 16
        if phase == 0:
            # Both ports write same address, full byte enables -> collision A wins
            a = corners[(i // 16) % len(corners)]
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 0xF, 'data_in_a': datas[i % len(datas)],
                'addr_b': a, 'en_b': 1, 'be_b': 0xF, 'data_in_b': datas[(i + 3) % len(datas)],
            }
        elif phase == 1:
            # Collision, A be=0, B be=0xF -> B wins
            a = corners[(i // 16) % len(corners)]
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 0x0, 'data_in_a': datas[i % len(datas)],
                'addr_b': a, 'en_b': 1, 'be_b': 0xF, 'data_in_b': datas[(i + 5) % len(datas)],
            }
        elif phase == 2:
            # Collision, complementary byte enables
            a = corners[(i // 16) % len(corners)]
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 0x5, 'data_in_a': datas[i % len(datas)],
                'addr_b': a, 'en_b': 1, 'be_b': 0xA, 'data_in_b': datas[(i + 7) % len(datas)],
            }
        elif phase == 3:
            # Collision, overlapping byte enables (A priority on overlap)
            a = corners[(i // 16) % len(corners)]
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 0x3, 'data_in_a': datas[i % len(datas)],
                'addr_b': a, 'en_b': 1, 'be_b': 0xC, 'data_in_b': datas[(i + 2) % len(datas)],
            }
        elif phase == 4:
            # Read from A, write to B different addr
            a = corners[(i // 16) % len(corners)]
            b = corners[((i // 16) + 3) % len(corners)]
            row = {
                'addr_a': a, 'en_a': 0, 'be_a': 0x0, 'data_in_a': 0,
                'addr_b': b, 'en_b': 1, 'be_b': 0xF, 'data_in_b': datas[i % len(datas)],
            }
        elif phase == 5:
            # Read from B, write to A
            a = corners[(i // 16) % len(corners)]
            b = corners[((i // 16) + 5) % len(corners)]
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 0xF, 'data_in_a': datas[(i + 1) % len(datas)],
                'addr_b': b, 'en_b': 0, 'be_b': 0x0, 'data_in_b': 0,
            }
        elif phase == 6:
            # Both read same address
            a = corners[(i // 16) % len(corners)]
            row = {
                'addr_a': a, 'en_a': 0, 'be_a': 0x0, 'data_in_a': 0,
                'addr_b': a, 'en_b': 0, 'be_b': 0x0, 'data_in_b': 0,
            }
        elif phase == 7:
            # Both write different addresses, full enables
            a = corners[(i // 16) % len(corners)]
            b = corners[((i // 16) + 1) % len(corners)]
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 0xF, 'data_in_a': datas[i % len(datas)],
                'addr_b': b, 'en_b': 1, 'be_b': 0xF, 'data_in_b': datas[(i + 4) % len(datas)],
            }
        elif phase == 8:
            # Partial byte writes both ports, different addresses
            a = corners[(i // 16) % len(corners)]
            b = corners[((i // 16) + 2) % len(corners)]
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': bes[i % len(bes)], 'data_in_a': datas[i % len(datas)],
                'addr_b': b, 'en_b': 1, 'be_b': bes[(i + 5) % len(bes)], 'data_in_b': datas[(i + 6) % len(datas)],
            }
        elif phase == 9:
            # en_a=0, en_b=0 (idle)
            a = corners[(i // 16) % len(corners)]
            b = corners[((i // 16) + 4) % len(corners)]
            row = {
                'addr_a': a, 'en_a': 0, 'be_a': 0xF, 'data_in_a': datas[i % len(datas)],
                'addr_b': b, 'en_b': 0, 'be_b': 0xF, 'data_in_b': datas[(i + 1) % len(datas)],
            }
        elif phase == 10:
            # Collision with en_a=0, en_b=1
            a = corners[(i // 16) % len(corners)]
            row = {
                'addr_a': a, 'en_a': 0, 'be_a': 0xF, 'data_in_a': datas[i % len(datas)],
                'addr_b': a, 'en_b': 1, 'be_b': 0xF, 'data_in_b': datas[(i + 2) % len(datas)],
            }
        elif phase == 11:
            # Collision with en_a=1, en_b=0
            a = corners[(i // 16) % len(corners)]
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 0xF, 'data_in_a': datas[i % len(datas)],
                'addr_b': a, 'en_b': 0, 'be_b': 0xF, 'data_in_b': datas[(i + 3) % len(datas)],
            }
        elif phase == 12:
            # Random-ish directed
            a = rng.randrange(0, 8192)
            b = rng.randrange(0, 8192)
            row = {
                'addr_a': a, 'en_a': rng.randrange(0, 2), 'be_a': rng.randrange(0, 16),
                'data_in_a': rng.randrange(0, 1 << 32),
                'addr_b': b, 'en_b': rng.randrange(0, 2), 'be_b': rng.randrange(0, 16),
                'data_in_b': rng.randrange(0, 1 << 32),
            }
        elif phase == 13:
            # Same address random enables
            a = rng.randrange(0, 8192)
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': rng.randrange(0, 16),
                'data_in_a': rng.randrange(0, 1 << 32),
                'addr_b': a, 'en_b': 1, 'be_b': rng.randrange(0, 16),
                'data_in_b': rng.randrange(0, 1 << 32),
            }
        elif phase == 14:
            # Sequential address sweep
            a = (i * 7) % 8192
            b = (i * 13 + 1) % 8192
            row = {
                'addr_a': a, 'en_a': 1, 'be_a': 0xF, 'data_in_a': (i * 0x01010101) & 0xFFFFFFFF,
                'addr_b': b, 'en_b': 1, 'be_b': 0xF, 'data_in_b': (i * 0x10101010) & 0xFFFFFFFF,
            }
        else:
            # Fully random
            row = {
                'addr_a': rng.randrange(0, 8192), 'en_a': rng.randrange(0, 2),
                'be_a': rng.randrange(0, 16), 'data_in_a': rng.randrange(0, 1 << 32),
                'addr_b': rng.randrange(0, 8192), 'en_b': rng.randrange(0, 2),
                'be_b': rng.randrange(0, 16), 'data_in_b': rng.randrange(0, 1 << 32),
            }
        rows.append(row)
    return rows

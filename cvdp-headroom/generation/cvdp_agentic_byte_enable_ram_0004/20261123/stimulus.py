def stimulus(rng, cycles):
    rows = []
    # Directed phase: fill a few addresses with known patterns, then read back.
    # Addresses chosen to exercise low/high bits and collision.
    addrs = [0, 1, 2, 3, 0x1FFF, 0x1000, 0x0FFF, 0x1234, 0x1ABC, 0x0555]
    # Phase 1: sequential writes to distinct addresses, full byte enables
    for i in range(min(cycles, 40)):
        a = addrs[i % len(addrs)]
        b = addrs[(i + 5) % len(addrs)]
        rows.append({
            'addr_a': a, 'en_a': 1, 'be_a': 0xF,
            'data_in_a': (0xA5A50000 | (i * 0x01010101)) & 0xFFFFFFFF,
            'addr_b': b, 'en_b': 1, 'be_b': 0xF,
            'data_in_b': (0x5A5A0000 | ((i + 7) * 0x01010101)) & 0xFFFFFFFF,
        })
    # Phase 2: reads (en=0) from those addresses, with occasional partial writes
    for i in range(min(cycles - len(rows), 40)):
        a = addrs[i % len(addrs)]
        b = addrs[(i + 3) % len(addrs)]
        rows.append({
            'addr_a': a, 'en_a': 0, 'be_a': 0,
            'data_in_a': 0,
            'addr_b': b, 'en_b': 0, 'be_b': 0,
            'data_in_b': 0,
        })
    # Phase 3: collision tests - same address, various be combinations
    be_pairs = [(0xF, 0xF), (0xF, 0x0), (0x0, 0xF), (0x3, 0xC), (0xC, 0x3),
                (0x1, 0xE), (0xE, 0x1), (0x5, 0xA), (0xA, 0x5), (0x0, 0x0)]
    for i in range(min(cycles - len(rows), 40)):
        bea, beb = be_pairs[i % len(be_pairs)]
        addr = addrs[i % 4]
        rows.append({
            'addr_a': addr, 'en_a': 1, 'be_a': bea,
            'data_in_a': (0xDEAD0000 | (i * 0x00010001)) & 0xFFFFFFFF,
            'addr_b': addr, 'en_b': 1, 'be_b': beb,
            'data_in_b': (0xBEEF0000 | (i * 0x00010001)) & 0xFFFFFFFF,
        })
    # Phase 4: partial byte writes to distinct addresses, then reads
    for i in range(min(cycles - len(rows), 40)):
        a = addrs[i % len(addrs)]
        b = addrs[(i + 2) % len(addrs)]
        bea = rng.randrange(16)
        beb = rng.randrange(16)
        rows.append({
            'addr_a': a, 'en_a': 1, 'be_a': bea,
            'data_in_a': rng.getrandbits(32),
            'addr_b': b, 'en_b': 1, 'be_b': beb,
            'data_in_b': rng.getrandbits(32),
        })
    # Phase 5: random exploration with mid-cycle changes
    while len(rows) < cycles:
        a = rng.randrange(8192)
        b = rng.randrange(8192)
        ena = rng.randrange(2)
        enb = rng.randrange(2)
        bea = rng.randrange(16) if ena else 0
        beb = rng.randrange(16) if enb else 0
        row = {
            'addr_a': a, 'en_a': ena, 'be_a': bea,
            'data_in_a': rng.getrandbits(32),
            'addr_b': b, 'en_b': enb, 'be_b': beb,
            'data_in_b': rng.getrandbits(32),
        }
        # Occasionally inject mid-cycle changes to exercise pipeline capture
        if rng.random() < 0.15:
            mid = {}
            if rng.random() < 0.5:
                mid['addr_a'] = rng.randrange(8192)
            if rng.random() < 0.5:
                mid['en_a'] = rng.randrange(2)
            if rng.random() < 0.5:
                mid['be_a'] = rng.randrange(16)
            if rng.random() < 0.5:
                mid['data_in_a'] = rng.getrandbits(32)
            if rng.random() < 0.5:
                mid['addr_b'] = rng.randrange(8192)
            if rng.random() < 0.5:
                mid['en_b'] = rng.randrange(2)
            if rng.random() < 0.5:
                mid['be_b'] = rng.randrange(16)
            if rng.random() < 0.5:
                mid['data_in_b'] = rng.getrandbits(32)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows[:cycles]

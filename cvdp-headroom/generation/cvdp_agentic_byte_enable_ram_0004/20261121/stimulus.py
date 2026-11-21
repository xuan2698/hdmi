def stimulus(rng, cycles):
    rows = []
    # Directed phase: fill a few addresses with known patterns, then read them back.
    # Addresses chosen to exercise low/high bits and collisions.
    hot = [0, 1, 2, 3, 0x1FFF, 0x1000, 0x0FFF, 0x1234, 0x1ABC, 0x0555]
    # Phase 1: write full words to hot addresses via port A
    for i in range(cycles):
        row = {}
        # default idle
        row['addr_a'] = 0
        row['en_a'] = 0
        row['be_a'] = 0
        row['data_in_a'] = 0
        row['addr_b'] = 0
        row['en_b'] = 0
        row['be_b'] = 0
        row['data_in_b'] = 0

        if i < 10:
            # full-word writes to hot addresses
            a = hot[i % len(hot)]
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 0xF
            row['data_in_a'] = (0xA5A50000 | (i * 0x1111)) & 0xFFFFFFFF
            # port B idle but address same to test no-collision when en_b=0
            row['addr_b'] = a
        elif i < 20:
            # byte-enable writes to hot addresses via port A
            a = hot[i % len(hot)]
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = (1 << (i % 4))
            row['data_in_a'] = (0xDEADBEEF ^ (i * 0x01010101)) & 0xFFFFFFFF
            row['addr_b'] = a
        elif i < 30:
            # read back hot addresses via both ports (en=0)
            a = hot[i % len(hot)]
            row['addr_a'] = a
            row['addr_b'] = hot[(i + 3) % len(hot)]
        elif i < 40:
            # collision: both ports write same address, different byte enables
            a = hot[i % len(hot)]
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = (0x3 << ((i % 2) * 2)) & 0xF
            row['data_in_a'] = (0x11111111 * (i + 1)) & 0xFFFFFFFF
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = (0xC >> ((i % 2) * 2)) & 0xF
            row['data_in_b'] = (0x22222222 * (i + 1)) & 0xFFFFFFFF
        elif i < 50:
            # collision with port A be=0 (port B should win)
            a = hot[i % len(hot)]
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 0
            row['data_in_a'] = 0xFFFFFFFF
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 0xF
            row['data_in_b'] = (0x33333333 * (i + 1)) & 0xFFFFFFFF
        elif i < 60:
            # collision with port B be=0 (port A should win)
            a = hot[i % len(hot)]
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 0xF
            row['data_in_a'] = (0x44444444 * (i + 1)) & 0xFFFFFFFF
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 0
            row['data_in_b'] = 0xFFFFFFFF
        elif i < 70:
            # independent writes to different addresses
            row['addr_a'] = hot[i % len(hot)]
            row['en_a'] = 1
            row['be_a'] = rng.randrange(1, 16)
            row['data_in_a'] = rng.getrandbits(32)
            row['addr_b'] = hot[(i + 5) % len(hot)]
            row['en_b'] = 1
            row['be_b'] = rng.randrange(1, 16)
            row['data_in_b'] = rng.getrandbits(32)
        elif i < 80:
            # reads with mid-cycle address changes
            row['addr_a'] = hot[i % len(hot)]
            row['addr_b'] = hot[(i + 2) % len(hot)]
            row['mid'] = {'addr_a': hot[(i + 7) % len(hot)]}
        else:
            # Random exploration with bias toward writes and collisions
            mode = rng.randrange(10)
            if mode < 4:
                # random independent writes
                row['addr_a'] = rng.randrange(8192)
                row['en_a'] = 1
                row['be_a'] = rng.randrange(1, 16)
                row['data_in_a'] = rng.getrandbits(32)
                row['addr_b'] = rng.randrange(8192)
                row['en_b'] = 1
                row['be_b'] = rng.randrange(1, 16)
                row['data_in_b'] = rng.getrandbits(32)
            elif mode < 6:
                # random collision
                a = rng.randrange(8192)
                row['addr_a'] = a
                row['en_a'] = 1
                row['be_a'] = rng.randrange(0, 16)
                row['data_in_a'] = rng.getrandbits(32)
                row['addr_b'] = a
                row['en_b'] = 1
                row['be_b'] = rng.randrange(0, 16)
                row['data_in_b'] = rng.getrandbits(32)
            elif mode < 8:
                # random reads
                row['addr_a'] = rng.randrange(8192)
                row['addr_b'] = rng.randrange(8192)
            else:
                # mixed read/write
                row['addr_a'] = rng.randrange(8192)
                row['en_a'] = rng.randrange(2)
                row['be_a'] = rng.randrange(16)
                row['data_in_a'] = rng.getrandbits(32)
                row['addr_b'] = rng.randrange(8192)
                row['en_b'] = rng.randrange(2)
                row['be_b'] = rng.randrange(16)
                row['data_in_b'] = rng.getrandbits(32)
            # occasionally add mid-cycle changes
            if rng.randrange(4) == 0:
                row['mid'] = {}
                if rng.randrange(2):
                    row['mid']['addr_a'] = rng.randrange(8192)
                if rng.randrange(2):
                    row['mid']['data_in_a'] = rng.getrandbits(32)
                if rng.randrange(2):
                    row['mid']['addr_b'] = rng.randrange(8192)
                if rng.randrange(2):
                    row['mid']['data_in_b'] = rng.getrandbits(32)
        rows.append(row)
    return rows

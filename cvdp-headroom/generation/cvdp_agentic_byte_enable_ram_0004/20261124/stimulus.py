def stimulus(rng, cycles):
    rows = []
    # Directed phase: establish known patterns, collisions, byte enables
    for i in range(cycles):
        row = {}
        # Base random values
        row['addr_a'] = rng.randrange(1 << 13)
        row['en_a'] = rng.randrange(2)
        row['be_a'] = rng.randrange(16)
        row['data_in_a'] = rng.randrange(1 << 32)
        row['addr_b'] = rng.randrange(1 << 13)
        row['en_b'] = rng.randrange(2)
        row['be_b'] = rng.randrange(16)
        row['data_in_b'] = rng.randrange(1 << 32)

        # Directed patterns
        if i < 40:
            # Fill a few addresses with full writes from A
            a = i % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 15
            row['data_in_a'] = (0xA5A50000 + i) & 0xFFFFFFFF
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 80:
            # Read back those addresses via B, no writes
            a = (i - 40) % 8
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 120:
            # Collision: same address, both enabled, various byte enables
            a = (i - 80) % 4
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = (i * 3) & 15
            row['data_in_a'] = 0x11111111 * ((i % 4) + 1)
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = (i * 5) & 15
            row['data_in_b'] = 0x22222222 * ((i % 4) + 1)
        elif i < 160:
            # Partial byte writes to distinct addresses
            a = (i - 120) % 8
            b = (a + 4) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 1 << ((i - 120) % 4)
            row['data_in_a'] = 0xDEADBEEF
            row['addr_b'] = b
            row['en_b'] = 1
            row['be_b'] = 1 << ((i - 119) % 4)
            row['data_in_b'] = 0xCAFEBABE
        elif i < 200:
            # Read back with alternating ports
            a = (i - 160) % 8
            if i % 2 == 0:
                row['addr_a'] = a
                row['en_a'] = 0
                row['be_a'] = 0
                row['data_in_a'] = 0
                row['addr_b'] = a
                row['en_b'] = 0
                row['be_b'] = 0
                row['data_in_b'] = 0
            else:
                row['addr_a'] = a
                row['en_a'] = 0
                row['be_a'] = 0
                row['data_in_a'] = 0
                row['addr_b'] = a
                row['en_b'] = 0
                row['be_b'] = 0
                row['data_in_b'] = 0
        elif i < 240:
            # Mid-cycle changes on some rows
            a = (i - 200) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 15
            row['data_in_a'] = 0x55555555
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
            if i % 3 == 0:
                row['mid'] = {
                    'addr_a': (a + 1) % 8,
                    'en_a': 0,
                    'be_a': 0,
                    'data_in_a': 0,
                }
        elif i < 280:
            # Same address, one enabled, one disabled
            a = (i - 240) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 15
            row['data_in_a'] = 0xAAAAAAAA
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 15
            row['data_in_b'] = 0xBBBBBBBB
        elif i < 320:
            # Same address, A disabled, B enabled
            a = (i - 280) % 8
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 15
            row['data_in_a'] = 0xCCCCCCCC
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 15
            row['data_in_b'] = 0xDDDDDDDD
        elif i < 360:
            # Collision with A be=0, B be=15
            a = (i - 320) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 0
            row['data_in_a'] = 0xEEEEEEEE
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 15
            row['data_in_b'] = 0xFFFFFFFF
        elif i < 400:
            # Collision with A be=15, B be=0
            a = (i - 360) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 15
            row['data_in_a'] = 0x12345678
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 0
            row['data_in_b'] = 0x87654321
        elif i < 440:
            # Collision with complementary byte enables
            a = (i - 400) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 0x5
            row['data_in_a'] = 0x11111111
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 0xA
            row['data_in_b'] = 0x22222222
        elif i < 480:
            # Collision with overlapping byte enables
            a = (i - 440) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 0x3
            row['data_in_a'] = 0x33333333
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 0xC
            row['data_in_b'] = 0x44444444
        elif i < 520:
            # Read back all addresses
            a = (i - 480) % 8
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 560:
            # Random with mid changes
            if i % 2 == 0:
                row['mid'] = {
                    'addr_a': rng.randrange(1 << 13),
                    'en_a': rng.randrange(2),
                    'be_a': rng.randrange(16),
                    'data_in_a': rng.randrange(1 << 32),
                }
        elif i < 600:
            # Address boundary values
            a = [0, 1, 2, 8191, 8190, 4095, 4096][(i - 560) % 7]
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 15
            row['data_in_a'] = 0xABCD0000 + i
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 640:
            # Read boundary values
            a = [0, 1, 2, 8191, 8190, 4095, 4096][(i - 600) % 7]
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 680:
            # Collision at boundary addresses
            a = [0, 8191, 4095, 4096][(i - 640) % 4]
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 15
            row['data_in_a'] = 0x99999999
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 15
            row['data_in_b'] = 0x77777777
        elif i < 720:
            # Read back boundary collisions
            a = [0, 8191, 4095, 4096][(i - 680) % 4]
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 760:
            # Single byte writes cycling through bytes
            a = (i - 720) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 1 << ((i - 720) % 4)
            row['data_in_a'] = 0x01020304 << (((i - 720) % 4) * 8)
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 800:
            # Read back single byte writes
            a = (i - 760) % 8
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 840:
            # Collision with single byte enables
            a = (i - 800) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 1 << ((i - 800) % 4)
            row['data_in_a'] = 0xAAAAAAAA
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 1 << (((i - 800) + 2) % 4)
            row['data_in_b'] = 0xBBBBBBBB
        elif i < 880:
            # Read back collision single bytes
            a = (i - 840) % 8
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 920:
            # Mid changes with collisions
            a = (i - 880) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 15
            row['data_in_a'] = 0x12345678
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 15
            row['data_in_b'] = 0x87654321
            if i % 4 == 0:
                row['mid'] = {
                    'addr_b': (a + 1) % 8,
                    'en_b': 0,
                }
        elif i < 960:
            # Read back mid change collisions
            a = (i - 920) % 8
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 1000:
            # Random with mid changes on both ports
            if i % 3 == 0:
                row['mid'] = {
                    'addr_a': rng.randrange(1 << 13),
                    'en_a': rng.randrange(2),
                    'be_a': rng.randrange(16),
                    'data_in_a': rng.randrange(1 << 32),
                    'addr_b': rng.randrange(1 << 13),
                    'en_b': rng.randrange(2),
                    'be_b': rng.randrange(16),
                    'data_in_b': rng.randrange(1 << 32),
                }
        elif i < 1040:
            # Same address, both enabled, A be=0, B be=0
            a = (i - 1000) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 0
            row['data_in_a'] = 0xFFFFFFFF
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 0
            row['data_in_b'] = 0x00000000
        elif i < 1080:
            # Read back
            a = (i - 1040) % 8
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 1120:
            # Collision with A be=0xF, B be=0xF, different data
            a = (i - 1080) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 15
            row['data_in_a'] = 0x00000000
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 15
            row['data_in_b'] = 0xFFFFFFFF
        elif i < 1160:
            # Read back
            a = (i - 1120) % 8
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 1200:
            # Collision with A be=0xF, B be=0xF, same data
            a = (i - 1160) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 15
            row['data_in_a'] = 0x55555555
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 15
            row['data_in_b'] = 0x55555555
        elif i < 1240:
            # Read back
            a = (i - 1200) % 8
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 1280:
            # Collision with A be=0x1, B be=0x2
            a = (i - 1240) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 1
            row['data_in_a'] = 0x11111111
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 2
            row['data_in_b'] = 0x22222222
        elif i < 1320:
            # Read back
            a = (i - 1280) % 8
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 1360:
            # Collision with A be=0x3, B be=0x3
            a = (i - 1320) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 3
            row['data_in_a'] = 0x33333333
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 3
            row['data_in_b'] = 0x44444444
        elif i < 1400:
            # Read back
            a = (i - 1360) % 8
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 1440:
            # Collision with A be=0x5, B be=0x5
            a = (i - 1400) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 5
            row['data_in_a'] = 0x55555555
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 5
            row['data_in_b'] = 0x66666666
        elif i < 1480:
            # Read back
            a = (i - 1440) % 8
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 1520:
            # Collision with A be=0xA, B be=0x5
            a = (i - 1480) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 10
            row['data_in_a'] = 0x77777777
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 5
            row['data_in_b'] = 0x88888888
        elif i < 1560:
            # Read back
            a = (i - 1520) % 8
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 1600:
            # Collision with A be=0xF, B be=0x0
            a = (i - 1560) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 15
            row['data_in_a'] = 0x99999999
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 0
            row['data_in_b'] = 0xAAAAAAAA
        elif i < 1640:
            # Read back
            a = (i - 1600) % 8
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 1680:
            # Collision with A be=0x0, B be=0xF
            a = (i - 1640) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 0
            row['data_in_a'] = 0xBBBBBBBB
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 15
            row['data_in_b'] = 0xCCCCCCCC
        elif i < 1720:
            # Read back
            a = (i - 1680) % 8
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 1760:
            # Collision with A be=0x1, B be=0x1
            a = (i - 1720) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 1
            row['data_in_a'] = 0xDDDDDDDD
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 1
            row['data_in_b'] = 0xEEEEEEEE
        elif i < 1800:
            # Read back
            a = (i - 1760) % 8
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 1840:
            # Collision with A be=0x2, B be=0x2
            a = (i - 1800) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 2
            row['data_in_a'] = 0xFFFFFFFF
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 2
            row['data_in_b'] = 0x00000000
        elif i < 1880:
            # Read back
            a = (i - 1840) % 8
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 1920:
            # Collision with A be=0x4, B be=0x4
            a = (i - 1880) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 4
            row['data_in_a'] = 0x12345678
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 4
            row['data_in_b'] = 0x87654321
        elif i < 1960:
            # Read back
            a = (i - 1920) % 8
            row['addr_a'] = a
            row['en_a'] = 0
            row['be_a'] = 0
            row['data_in_a'] = 0
            row['addr_b'] = a
            row['en_b'] = 0
            row['be_b'] = 0
            row['data_in_b'] = 0
        elif i < 2000:
            # Collision with A be=0x8, B be=0x8
            a = (i - 1960) % 8
            row['addr_a'] = a
            row['en_a'] = 1
            row['be_a'] = 8
            row['data_in_a'] = 0xABCDEF01
            row['addr_b'] = a
            row['en_b'] = 1
            row['be_b'] = 8
            row['data_in_b'] = 0x10FEDCBA
        else:
            # Final random with mid changes
            if i % 5 == 0:
                row['mid'] = {
                    'addr_a': rng.randrange(1 << 13),
                    'en_a': rng.randrange(2),
                    'be_a': rng.randrange(16),
                    'data_in_a': rng.randrange(1 << 32),
                    'addr_b': rng.randrange(1 << 13),
                    'en_b': rng.randrange(2),
                    'be_b': rng.randrange(16),
                    'data_in_b': rng.randrange(1 << 32),
                }

        rows.append(row)
    return rows

def stimulus(rng, cycles):
    rows = []
    # Phase plan (cycle indices):
    # 0-3 reset, 4-60 normal tx, 61-100 back-to-back, 101-140 mid-data changes,
    # 141-180 disable mid-tx, 181-220 clear mid-tx, 221-260 fault, 261-300 recover,
    # 301-360 extreme data, 361-420 fault+clear combos, 421+ random
    data_pool = [0x0000, 0xFFFF, 0x8000, 0x0001, 0xAAAA, 0x5555, 0x1234, 0xDEAD,
                 0x00FF, 0xFF00, 0x0002, 0x4000, 0x0100, 0x0080, 0x7FFF, 0x8001]
    for c in range(cycles):
        row = {'i_rst_b': 1, 'i_data_in': 0, 'i_enable': 0, 'i_fault': 0, 'i_clear': 0}
        if c < 4:
            row['i_rst_b'] = 0
            row['i_data_in'] = rng.randrange(1 << 16)
            rows.append(row)
            continue
        if c < 60:
            row['i_enable'] = 1
            row['i_data_in'] = data_pool[c % len(data_pool)]
        elif c < 100:
            row['i_enable'] = 1
            row['i_data_in'] = rng.randrange(1 << 16)
        elif c < 140:
            row['i_enable'] = 1
            row['i_data_in'] = data_pool[(c // 3) % len(data_pool)]
            if c % 5 == 0:
                row['mid'] = {'i_data_in': rng.randrange(1 << 16)}
        elif c < 180:
            row['i_enable'] = 0 if (c % 20) < 6 else 1
            row['i_data_in'] = data_pool[c % len(data_pool)]
        elif c < 220:
            row['i_enable'] = 1
            row['i_clear'] = 1 if (c % 15) < 3 else 0
            row['i_data_in'] = data_pool[(c // 2) % len(data_pool)]
        elif c < 260:
            row['i_enable'] = 1
            row['i_fault'] = 1 if (c % 25) < 8 else 0
            row['i_data_in'] = data_pool[c % len(data_pool)]
        elif c < 300:
            row['i_enable'] = 1
            row['i_clear'] = 1 if (c % 10) < 2 else 0
            row['i_data_in'] = data_pool[(c + 3) % len(data_pool)]
        elif c < 360:
            row['i_enable'] = 1
            row['i_data_in'] = [0x0000, 0xFFFF, 0x8000, 0x0001, 0x0002, 0x4000][c % 6]
        elif c < 420:
            row['i_enable'] = 1
            row['i_fault'] = 1 if (c % 12) < 4 else 0
            row['i_clear'] = 1 if (c % 12) >= 8 else 0
            row['i_data_in'] = data_pool[(c * 7) % len(data_pool)]
        else:
            row['i_enable'] = 1 if rng.random() < 0.85 else 0
            row['i_fault'] = 1 if rng.random() < 0.08 else 0
            row['i_clear'] = 1 if rng.random() < 0.08 else 0
            row['i_data_in'] = rng.randrange(1 << 16)
            if rng.random() < 0.15:
                row['mid'] = {'i_data_in': rng.randrange(1 << 16)}
        rows.append(row)
    return rows

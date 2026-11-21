def stimulus(rng, cycles):
    rows = []
    # Phase plan (indices into rows)
    # 0-3: reset low then release
    # 4-30: normal transmissions with various data
    # 31-60: back-to-back transmissions
    # 61-90: disable mid-transmission
    # 91-120: clear mid-transmission
    # 121-150: fault injection and recovery
    # 151-200: extreme data patterns
    # 201+: random exploration
    data_patterns = [
        0x0000, 0xFFFF, 0x0001, 0x8000, 0xAAAA, 0x5555,
        0x00FF, 0xFF00, 0x1234, 0xDEAD, 0xBEEF, 0xCAFE,
        0x0002, 0x4000, 0x0100, 0x0080, 0x7FFF, 0x8001,
    ]
    for i in range(cycles):
        row = {
            'i_rst_b': 1,
            'i_data_in': 0,
            'i_enable': 0,
            'i_fault': 0,
            'i_clear': 0,
        }
        mid = {}
        if i < 3:
            row['i_rst_b'] = 0
            row['i_enable'] = 0
        elif i < 4:
            row['i_rst_b'] = 1
            row['i_enable'] = 0
        elif i < 30:
            # Normal transmissions: enable high, data varies
            row['i_enable'] = 1
            row['i_data_in'] = data_patterns[(i - 4) % len(data_patterns)]
        elif i < 60:
            # Back-to-back: keep enable high, change data
            row['i_enable'] = 1
            row['i_data_in'] = data_patterns[(i * 7 + 3) % len(data_patterns)]
        elif i < 90:
            # Disable mid-transmission: toggle enable
            row['i_enable'] = 1 if (i % 5 != 0) else 0
            row['i_data_in'] = data_patterns[(i * 3) % len(data_patterns)]
        elif i < 120:
            # Clear mid-transmission
            row['i_enable'] = 1
            row['i_data_in'] = data_patterns[(i * 5) % len(data_patterns)]
            if i % 7 == 0:
                mid['i_clear'] = 1
        elif i < 150:
            # Fault injection and recovery
            row['i_enable'] = 1
            row['i_data_in'] = data_patterns[(i * 11) % len(data_patterns)]
            if i % 9 == 0:
                row['i_fault'] = 1
            if i % 9 == 4:
                row['i_clear'] = 1
        elif i < 200:
            # Extreme data patterns
            row['i_enable'] = 1
            row['i_data_in'] = data_patterns[(i - 151) % len(data_patterns)]
        else:
            # Random exploration
            row['i_rst_b'] = 1 if rng.random() > 0.02 else 0
            row['i_enable'] = 1 if rng.random() > 0.15 else 0
            row['i_fault'] = 1 if rng.random() > 0.92 else 0
            row['i_clear'] = 1 if rng.random() > 0.90 else 0
            row['i_data_in'] = rng.randrange(0, 1 << 16)
            if rng.random() > 0.85:
                mid['i_enable'] = rng.randrange(0, 2)
            if rng.random() > 0.90:
                mid['i_clear'] = rng.randrange(0, 2)
            if rng.random() > 0.93:
                mid['i_fault'] = rng.randrange(0, 2)
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows

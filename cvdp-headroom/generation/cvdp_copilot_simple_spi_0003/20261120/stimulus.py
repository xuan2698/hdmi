def stimulus(rng, cycles):
    rows = []
    # Phase plan (roughly):
    # 0-3 reset, 4-40 normal tx, 41-80 back-to-back, 81-120 mid-data changes,
    # 121-160 disable mid-tx, 161-200 clear mid-tx, 201-240 fault, 241-280 recovery,
    # 281-320 extreme data, 321+ random exploration.
    for c in range(cycles):
        row = {
            'i_rst_b': 1,
            'i_data_in': 0,
            'i_enable': 0,
            'i_fault': 0,
            'i_clear': 0,
        }
        mid = {}

        if c < 3:
            row['i_rst_b'] = 0
            row['i_enable'] = 0
            row['i_data_in'] = 0
        elif c < 40:
            # Normal transmission: enable high, varied data
            row['i_enable'] = 1
            if c == 3:
                row['i_data_in'] = 0xA5A5
            elif c == 4:
                row['i_data_in'] = 0x1234
            elif c == 5:
                row['i_data_in'] = 0xFFFF
            elif c == 6:
                row['i_data_in'] = 0x0000
            else:
                row['i_data_in'] = rng.randrange(0, 1 << 16)
        elif c < 80:
            # Back-to-back transmissions, keep enable high, change data
            row['i_enable'] = 1
            row['i_data_in'] = rng.randrange(0, 1 << 16)
        elif c < 120:
            # Mid-cycle data changes during transmission
            row['i_enable'] = 1
            row['i_data_in'] = rng.randrange(0, 1 << 16)
            if c % 3 == 0:
                mid['i_data_in'] = rng.randrange(0, 1 << 16)
        elif c < 160:
            # Disable mid-transmission
            row['i_enable'] = 1
            row['i_data_in'] = rng.randrange(0, 1 << 16)
            if c % 5 == 0:
                mid['i_enable'] = 0
            elif c % 5 == 1:
                row['i_enable'] = 0
        elif c < 200:
            # Clear mid-transmission
            row['i_enable'] = 1
            row['i_data_in'] = rng.randrange(0, 1 << 16)
            if c % 4 == 0:
                mid['i_clear'] = 1
            elif c % 4 == 1:
                row['i_clear'] = 1
        elif c < 240:
            # Fault injection
            row['i_enable'] = 1
            row['i_data_in'] = rng.randrange(0, 1 << 16)
            if c % 6 == 0:
                row['i_fault'] = 1
            elif c % 6 == 1:
                mid['i_fault'] = 1
            elif c % 6 == 2:
                row['i_fault'] = 1
                row['i_clear'] = 1
        elif c < 280:
            # Recovery from fault via clear/reset
            row['i_enable'] = 1
            row['i_data_in'] = rng.randrange(0, 1 << 16)
            if c % 7 == 0:
                row['i_clear'] = 1
            elif c % 7 == 1:
                row['i_rst_b'] = 0
            elif c % 7 == 2:
                row['i_fault'] = 1
                mid['i_clear'] = 1
        elif c < 320:
            # Extreme data values
            row['i_enable'] = 1
            extremes = [0x0000, 0xFFFF, 0x0001, 0x8000, 0x0002, 0x4000, 0xAAAA, 0x5555]
            row['i_data_in'] = extremes[c % len(extremes)]
        else:
            # Random exploration with occasional control toggles
            row['i_enable'] = 1 if rng.random() < 0.85 else 0
            row['i_data_in'] = rng.randrange(0, 1 << 16)
            r = rng.random()
            if r < 0.05:
                row['i_fault'] = 1
            elif r < 0.10:
                row['i_clear'] = 1
            elif r < 0.13:
                row['i_rst_b'] = 0
            if rng.random() < 0.10:
                mid['i_data_in'] = rng.randrange(0, 1 << 16)
            if rng.random() < 0.05:
                mid['i_enable'] = rng.randrange(0, 2)
            if rng.random() < 0.03:
                mid['i_clear'] = 1
            if rng.random() < 0.03:
                mid['i_fault'] = 1

        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows

def stimulus(rng, cycles):
    rows = []
    # Directed corner vectors (a, b, mode) as unsigned 8-bit
    corners = [
        (5, 10, 0), (15, 0xFB, 0), (127, 0, 0), (127, 1, 0),
        (0x80, 0xFF, 0), (20, 5, 1), (5, 20, 1), (127, 0xFF, 1),
        (0x80, 0, 1), (0x80, 0x80, 0), (0x7F, 0x7F, 0),
        (0x80, 0x7F, 1), (0x7F, 0x80, 1), (0, 0, 0), (0, 0, 1),
        (0xFF, 0xFF, 0), (0xFF, 0x01, 0), (0x01, 0xFF, 1),
        (0x7F, 0xFF, 0), (0x80, 0x01, 1), (0x40, 0x40, 0),
        (0xC0, 0xC0, 0), (0x40, 0xC0, 1), (0xC0, 0x40, 1),
    ]
    ci = 0
    # Phase plan: reset, idle, normal ops, clear, reset mid-op, enable=0, random
    for c in range(cycles):
        row = {
            'i_rst_n': 1, 'i_start': 0, 'i_enable': 1, 'i_mode': 0,
            'i_clear': 0, 'i_operand_a': 0, 'i_operand_b': 0,
        }
        phase = c % 40
        if c < 3:
            row['i_rst_n'] = 0
        elif c < 6:
            row['i_rst_n'] = 1
            row['i_enable'] = 0
        elif phase < 4:
            # start pulse sequence
            row['i_start'] = 1 if phase == 0 else 0
            a, b, m = corners[ci % len(corners)]
            ci += 1
            row['i_operand_a'] = a
            row['i_operand_b'] = b
            row['i_mode'] = m
        elif phase < 8:
            # continue holding operands, no start
            a, b, m = corners[(ci - 1) % len(corners)]
            row['i_operand_a'] = a
            row['i_operand_b'] = b
            row['i_mode'] = m
        elif phase == 8:
            row['i_clear'] = 1
        elif phase == 9:
            row['i_clear'] = 1
            row['i_start'] = 1
        elif phase == 10:
            row['i_rst_n'] = 0
        elif phase == 11:
            row['i_rst_n'] = 1
            row['i_start'] = 1
        elif phase == 12:
            row['i_enable'] = 0
            row['i_start'] = 1
        elif phase == 13:
            row['i_enable'] = 0
        elif phase == 14:
            row['i_enable'] = 1
            row['i_start'] = 1
        elif phase < 20:
            a, b, m = corners[ci % len(corners)]
            ci += 1
            row['i_operand_a'] = a
            row['i_operand_b'] = b
            row['i_mode'] = m
            row['i_start'] = 1 if phase == 15 else 0
        else:
            # random exploration
            row['i_operand_a'] = rng.randrange(256)
            row['i_operand_b'] = rng.randrange(256)
            row['i_mode'] = rng.randrange(2)
            row['i_start'] = 1 if rng.random() < 0.3 else 0
            row['i_enable'] = 1 if rng.random() < 0.85 else 0
            row['i_clear'] = 1 if rng.random() < 0.05 else 0
            row['i_rst_n'] = 0 if rng.random() < 0.03 else 1
        # occasional mid-cycle changes
        if rng.random() < 0.15:
            mid = {}
            if rng.random() < 0.5:
                mid['i_start'] = rng.randrange(2)
            if rng.random() < 0.4:
                mid['i_clear'] = rng.randrange(2)
            if rng.random() < 0.3:
                mid['i_enable'] = rng.randrange(2)
            if rng.random() < 0.3:
                mid['i_mode'] = rng.randrange(2)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows

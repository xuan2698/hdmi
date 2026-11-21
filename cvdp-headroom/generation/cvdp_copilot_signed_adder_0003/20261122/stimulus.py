def stimulus(rng, cycles):
    rows = []
    # Directed corner operands (8-bit signed)
    corners = [0x00, 0x01, 0x7F, 0x80, 0xFF, 0xFE, 0x40, 0xC0, 0x55, 0xAA]
    # Build a directed sequence of (rst_n, start, enable, mode, clear, a, b)
    seq = []
    # Reset pulse
    seq.append((0, 0, 0, 0, 0, 0, 0))
    seq.append((0, 0, 0, 0, 0, 0, 0))
    # Basic add: 5 + 10
    seq.append((1, 1, 1, 0, 0, 5, 10))
    seq.append((1, 0, 1, 0, 0, 5, 10))
    seq.append((1, 0, 1, 0, 0, 5, 10))
    seq.append((1, 0, 1, 0, 0, 5, 10))
    # Positive + negative
    seq.append((1, 1, 1, 0, 0, 15, 0xFB))
    seq.append((1, 0, 1, 0, 0, 15, 0xFB))
    seq.append((1, 0, 1, 0, 0, 15, 0xFB))
    seq.append((1, 0, 1, 0, 0, 15, 0xFB))
    # Boundary no overflow
    seq.append((1, 1, 1, 0, 0, 127, 0))
    seq.append((1, 0, 1, 0, 0, 127, 0))
    seq.append((1, 0, 1, 0, 0, 127, 0))
    seq.append((1, 0, 1, 0, 0, 127, 0))
    # Positive overflow
    seq.append((1, 1, 1, 0, 0, 127, 1))
    seq.append((1, 0, 1, 0, 0, 127, 1))
    seq.append((1, 0, 1, 0, 0, 127, 1))
    seq.append((1, 0, 1, 0, 0, 127, 1))
    # Negative overflow
    seq.append((1, 1, 1, 0, 0, 0x80, 0xFF))
    seq.append((1, 0, 1, 0, 0, 0x80, 0xFF))
    seq.append((1, 0, 1, 0, 0, 0x80, 0xFF))
    seq.append((1, 0, 1, 0, 0, 0x80, 0xFF))
    # Basic subtraction
    seq.append((1, 1, 1, 1, 0, 20, 5))
    seq.append((1, 0, 1, 1, 0, 20, 5))
    seq.append((1, 0, 1, 1, 0, 20, 5))
    seq.append((1, 0, 1, 1, 0, 20, 5))
    # Negative result subtraction
    seq.append((1, 1, 1, 1, 0, 5, 20))
    seq.append((1, 0, 1, 1, 0, 5, 20))
    seq.append((1, 0, 1, 1, 0, 5, 20))
    seq.append((1, 0, 1, 1, 0, 5, 20))
    # Subtraction overflow
    seq.append((1, 1, 1, 1, 0, 127, 0xFF))
    seq.append((1, 0, 1, 1, 0, 127, 0xFF))
    seq.append((1, 0, 1, 1, 0, 127, 0xFF))
    seq.append((1, 0, 1, 1, 0, 127, 0xFF))
    # Enable low, start pulse ignored
    seq.append((1, 1, 0, 0, 0, 10, 20))
    seq.append((1, 0, 0, 0, 0, 10, 20))
    seq.append((1, 0, 0, 0, 0, 10, 20))
    # Clear during operation
    seq.append((1, 1, 1, 0, 0, 30, 40))
    seq.append((1, 0, 1, 0, 1, 30, 40))
    seq.append((1, 0, 1, 0, 0, 30, 40))
    seq.append((1, 0, 1, 0, 0, 30, 40))
    # Reset during operation
    seq.append((1, 1, 1, 0, 0, 50, 60))
    seq.append((0, 0, 1, 0, 0, 50, 60))
    seq.append((1, 0, 1, 0, 0, 50, 60))
    seq.append((1, 0, 1, 0, 0, 50, 60))
    # Enable drop mid-operation
    seq.append((1, 1, 1, 0, 0, 70, 80))
    seq.append((1, 0, 0, 0, 0, 70, 80))
    seq.append((1, 0, 1, 0, 0, 70, 80))
    seq.append((1, 0, 1, 0, 0, 70, 80))
    # Corner pairs add and sub
    for m in (0, 1):
        for a in corners:
            for b in corners:
                seq.append((1, 1, 1, m, 0, a, b))
                seq.append((1, 0, 1, m, 0, a, b))
                seq.append((1, 0, 1, m, 0, a, b))
                seq.append((1, 0, 1, m, 0, a, b))
    # Fill remaining with random exploration
    idx = 0
    n = len(seq)
    while len(rows) < cycles:
        if idx < n:
            r = seq[idx]
            idx += 1
        else:
            # Random with occasional mid changes
            rst = 1 if rng.random() > 0.02 else 0
            start = 1 if rng.random() < 0.35 else 0
            en = 1 if rng.random() < 0.85 else 0
            mode = rng.randint(0, 1)
            clr = 1 if rng.random() < 0.05 else 0
            a = rng.randint(0, 255)
            b = rng.randint(0, 255)
            r = (rst, start, en, mode, clr, a, b)
        row = {
            'i_rst_n': r[0],
            'i_start': r[1],
            'i_enable': r[2],
            'i_mode': r[3],
            'i_clear': r[4],
            'i_operand_a': r[5],
            'i_operand_b': r[6],
        }
        # Occasionally inject mid-cycle changes
        if rng.random() < 0.15:
            mid = {}
            if rng.random() < 0.5:
                mid['i_start'] = rng.randint(0, 1)
            if rng.random() < 0.5:
                mid['i_enable'] = rng.randint(0, 1)
            if rng.random() < 0.3:
                mid['i_clear'] = rng.randint(0, 1)
            if rng.random() < 0.3:
                mid['i_mode'] = rng.randint(0, 1)
            if rng.random() < 0.4:
                mid['i_operand_a'] = rng.randint(0, 255)
            if rng.random() < 0.4:
                mid['i_operand_b'] = rng.randint(0, 255)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows

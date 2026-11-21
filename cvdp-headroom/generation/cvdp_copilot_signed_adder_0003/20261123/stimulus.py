def stimulus(rng, cycles):
    rows = []
    # Directed corner operands (8-bit signed)
    corners = [0x00, 0x01, 0x7F, 0x80, 0xFF, 0xFE, 0x40, 0xC0, 0x55, 0xAA]
    # Build a directed sequence of (rst, start, enable, mode, clear, a, b)
    seq = []
    # Reset pulse
    seq.append((0,0,0,0,0,0,0))
    seq.append((1,0,0,0,0,0,0))
    # Basic add
    seq.append((1,1,1,0,0,5,10))
    seq.append((1,0,1,0,0,5,10))
    seq.append((1,0,1,0,0,5,10))
    seq.append((1,0,1,0,0,5,10))
    # Positive + negative
    seq.append((1,1,1,0,0,15,0xFB))
    seq.append((1,0,1,0,0,15,0xFB))
    seq.append((1,0,1,0,0,15,0xFB))
    seq.append((1,0,1,0,0,15,0xFB))
    # Boundary no overflow
    seq.append((1,1,1,0,0,0x7F,0x00))
    seq.append((1,0,1,0,0,0x7F,0x00))
    seq.append((1,0,1,0,0,0x7F,0x00))
    seq.append((1,0,1,0,0,0x7F,0x00))
    # Positive overflow
    seq.append((1,1,1,0,0,0x7F,0x01))
    seq.append((1,0,1,0,0,0x7F,0x01))
    seq.append((1,0,1,0,0,0x7F,0x01))
    seq.append((1,0,1,0,0,0x7F,0x01))
    # Negative overflow
    seq.append((1,1,1,0,0,0x80,0xFF))
    seq.append((1,0,1,0,0,0x80,0xFF))
    seq.append((1,0,1,0,0,0x80,0xFF))
    seq.append((1,0,1,0,0,0x80,0xFF))
    # Basic subtraction
    seq.append((1,1,1,1,0,20,5))
    seq.append((1,0,1,1,0,20,5))
    seq.append((1,0,1,1,0,20,5))
    seq.append((1,0,1,1,0,20,5))
    # Negative result subtraction
    seq.append((1,1,1,1,0,5,20))
    seq.append((1,0,1,1,0,5,20))
    seq.append((1,0,1,1,0,5,20))
    seq.append((1,0,1,1,0,5,20))
    # Subtraction overflow
    seq.append((1,1,1,1,0,0x7F,0xFF))
    seq.append((1,0,1,1,0,0x7F,0xFF))
    seq.append((1,0,1,1,0,0x7F,0xFF))
    seq.append((1,0,1,1,0,0x7F,0xFF))
    # Enable low, start pulse ignored
    seq.append((1,1,0,0,0,0x12,0x34))
    seq.append((1,0,0,0,0,0x12,0x34))
    seq.append((1,0,0,0,0,0x12,0x34))
    # Clear during operation
    seq.append((1,1,1,0,0,0x11,0x22))
    seq.append((1,0,1,0,1,0x11,0x22))
    seq.append((1,0,1,0,0,0x11,0x22))
    seq.append((1,0,1,0,0,0x11,0x22))
    # Reset during operation
    seq.append((1,1,1,0,0,0x33,0x44))
    seq.append((0,0,1,0,0,0x33,0x44))
    seq.append((1,0,1,0,0,0x33,0x44))
    seq.append((1,0,1,0,0,0x33,0x44))
    # Clear in IDLE
    seq.append((1,0,1,0,1,0,0))
    seq.append((1,0,1,0,0,0,0))
    # Back-to-back operations
    for _ in range(4):
        seq.append((1,1,1,0,0,0x10,0x20))
        seq.append((1,0,1,0,0,0x10,0x20))
        seq.append((1,0,1,0,0,0x10,0x20))
        seq.append((1,0,1,0,0,0x10,0x20))
    # Fill remaining with random exploration
    while len(seq) < cycles:
        r = rng.random()
        if r < 0.05:
            rst = 0
        else:
            rst = 1
        start = 1 if rng.random() < 0.35 else 0
        enable = 1 if rng.random() < 0.85 else 0
        mode = 1 if rng.random() < 0.5 else 0
        clear = 1 if rng.random() < 0.08 else 0
        if rng.random() < 0.5:
            a = corners[rng.randrange(len(corners))]
        else:
            a = rng.randrange(256)
        if rng.random() < 0.5:
            b = corners[rng.randrange(len(corners))]
        else:
            b = rng.randrange(256)
        seq.append((rst, start, enable, mode, clear, a, b))
    # Trim/pad to exactly cycles
    seq = seq[:cycles]
    while len(seq) < cycles:
        seq.append((1,0,1,0,0,0,0))
    for (rst, start, enable, mode, clear, a, b) in seq:
        row = {
            'i_rst_n': rst,
            'i_start': start,
            'i_enable': enable,
            'i_mode': mode,
            'i_clear': clear,
            'i_operand_a': a & 0xFF,
            'i_operand_b': b & 0xFF,
        }
        rows.append(row)
    return rows

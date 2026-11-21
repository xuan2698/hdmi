def stimulus(rng, cycles):
    rows = []
    # Directed corner operands (8-bit signed)
    corners = [0x00, 0x01, 0x7F, 0x80, 0xFF, 0x02, 0xFE, 0x40, 0xC0, 0x55, 0xAA]
    # Build a directed sequence of (rst_n, start, enable, mode, clear, a, b)
    seq = []
    # Reset pulse
    seq.append((0,0,0,0,0,0,0))
    seq.append((1,0,0,0,0,0,0))
    # Basic add: 5+10
    seq.append((1,1,1,0,0,5,10))
    seq.append((1,0,1,0,0,5,10))
    seq.append((1,0,1,0,0,5,10))
    seq.append((1,0,1,0,0,5,10))
    # Positive + negative
    seq.append((1,1,1,0,0,15,0xFB))
    seq.append((1,0,1,0,0,15,0xFB))
    seq.append((1,0,1,0,0,15,0xFB))
    seq.append((1,0,1,0,0,15,0xFB))
    # Boundary no overflow 127+0
    seq.append((1,1,1,0,0,0x7F,0))
    seq.append((1,0,1,0,0,0x7F,0))
    seq.append((1,0,1,0,0,0x7F,0))
    seq.append((1,0,1,0,0,0x7F,0))
    # Positive overflow 127+1
    seq.append((1,1,1,0,0,0x7F,1))
    seq.append((1,0,1,0,0,0x7F,1))
    seq.append((1,0,1,0,0,0x7F,1))
    seq.append((1,0,1,0,0,0x7F,1))
    # Negative overflow -128 + -1
    seq.append((1,1,1,0,0,0x80,0xFF))
    seq.append((1,0,1,0,0,0x80,0xFF))
    seq.append((1,0,1,0,0,0x80,0xFF))
    seq.append((1,0,1,0,0,0x80,0xFF))
    # Basic subtraction 20-5
    seq.append((1,1,1,1,0,20,5))
    seq.append((1,0,1,1,0,20,5))
    seq.append((1,0,1,1,0,20,5))
    seq.append((1,0,1,1,0,20,5))
    # Negative result 5-20
    seq.append((1,1,1,1,0,5,20))
    seq.append((1,0,1,1,0,5,20))
    seq.append((1,0,1,1,0,5,20))
    seq.append((1,0,1,1,0,5,20))
    # Subtraction overflow 127 - (-1)
    seq.append((1,1,1,1,0,0x7F,0xFF))
    seq.append((1,0,1,1,0,0x7F,0xFF))
    seq.append((1,0,1,1,0,0x7F,0xFF))
    seq.append((1,0,1,1,0,0x7F,0xFF))
    # Enable=0, start pulse (no transition)
    seq.append((1,1,0,0,0,0x12,0x34))
    seq.append((1,0,0,0,0,0x12,0x34))
    seq.append((1,0,0,0,0,0x12,0x34))
    # Clear during operation
    seq.append((1,1,1,0,0,0x11,0x22))
    seq.append((1,0,1,0,1,0x11,0x22))
    seq.append((1,0,1,0,0,0x11,0x22))
    # Reset during operation
    seq.append((1,1,1,0,0,0x33,0x44))
    seq.append((0,0,1,0,0,0x33,0x44))
    seq.append((1,0,1,0,0,0x33,0x44))
    # Clear in IDLE
    seq.append((1,0,1,0,1,0,0))
    seq.append((1,0,1,0,0,0,0))

    i = 0
    n = len(seq)
    while len(rows) < cycles:
        if i < n:
            r = seq[i]
            i += 1
        else:
            # Random exploration with occasional directed corners
            rst = 1 if rng.random() > 0.02 else 0
            en = 1 if rng.random() > 0.15 else 0
            st = 1 if rng.random() > 0.5 else 0
            md = rng.randint(0, 1)
            cl = 1 if rng.random() > 0.92 else 0
            if rng.random() < 0.4:
                a = corners[rng.randrange(len(corners))]
                b = corners[rng.randrange(len(corners))]
            else:
                a = rng.randrange(256)
                b = rng.randrange(256)
            r = (rst, st, en, md, cl, a, b)
        row = {
            'i_rst_n': r[0],
            'i_start': r[1],
            'i_enable': r[2],
            'i_mode': r[3],
            'i_clear': r[4],
            'i_operand_a': r[5],
            'i_operand_b': r[6],
        }
        # Occasionally inject mid-cycle changes on operands/mode
        if rng.random() < 0.15:
            row['mid'] = {
                'i_operand_a': rng.randrange(256),
                'i_operand_b': rng.randrange(256),
                'i_mode': rng.randint(0, 1),
            }
        rows.append(row)
    return rows

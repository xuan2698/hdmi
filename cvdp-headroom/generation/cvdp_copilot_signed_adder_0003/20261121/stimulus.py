def stimulus(rng, cycles):
    rows = []
    def add(rst=1, start=0, en=1, mode=0, clr=0, a=0, b=0, mid=None):
        r = {'i_rst_n': rst, 'i_start': start, 'i_enable': en, 'i_mode': mode,
             'i_clear': clr, 'i_operand_a': a & 0xFF, 'i_operand_b': b & 0xFF}
        if mid:
            r['mid'] = mid
        rows.append(r)

    # Reset sequence
    add(rst=0)
    add(rst=0, start=1, en=1)
    add(rst=1)
    add(rst=1, start=1, en=1, a=5, b=10)
    add(rst=1, start=0, en=1, a=5, b=10)
    add(rst=1, start=0, en=1, a=5, b=10)
    add(rst=1, start=0, en=1, a=5, b=10)

    # Directed scenarios: (mode, a, b)
    directed = [
        (0, 5, 10), (0, 15, 0xFB), (0, 127, 0), (0, 127, 1), (0, 0x80, 0xFF),
        (0, 0x80, 0x80), (0, 0x7F, 0x7F), (0, 0xFF, 0xFF), (0, 0, 0),
        (1, 20, 5), (1, 5, 20), (1, 127, 0xFF), (1, 0x80, 1), (1, 0x80, 0x80),
        (1, 0x7F, 0x80), (1, 0, 0), (1, 0xFF, 0x7F), (1, 0x80, 0x7F),
        (0, 0x40, 0x40), (0, 0xC0, 0xC0), (1, 0x40, 0xC0), (1, 0xC0, 0x40),
    ]

    # Run directed scenarios with proper handshake
    for mode, a, b in directed:
        add(rst=1, start=1, en=1, mode=mode, a=a, b=b)
        add(rst=1, start=0, en=1, mode=mode, a=a, b=b)
        add(rst=1, start=0, en=1, mode=mode, a=a, b=b)
        add(rst=1, start=0, en=1, mode=mode, a=a, b=b)
        add(rst=1, start=0, en=1, mode=mode, a=a, b=b)

    # Clear during operation
    add(rst=1, start=1, en=1, mode=0, a=10, b=20)
    add(rst=1, start=0, en=1, mode=0, a=10, b=20, clr=1)
    add(rst=1, start=0, en=1, mode=0, a=10, b=20)
    add(rst=1, start=0, en=1, mode=0, a=10, b=20)

    # Reset during operation
    add(rst=1, start=1, en=1, mode=1, a=50, b=30)
    add(rst=0, start=0, en=1, mode=1, a=50, b=30)
    add(rst=1, start=0, en=1, mode=1, a=50, b=30)

    # Disabled enable
    add(rst=1, start=1, en=0, mode=0, a=1, b=2)
    add(rst=1, start=1, en=0, mode=0, a=1, b=2)
    add(rst=1, start=0, en=0, mode=0, a=1, b=2)

    # Enable deassert mid-operation
    add(rst=1, start=1, en=1, mode=0, a=7, b=8)
    add(rst=1, start=0, en=0, mode=0, a=7, b=8)
    add(rst=1, start=0, en=1, mode=0, a=7, b=8)

    # Mid-cycle changes
    add(rst=1, start=1, en=1, mode=0, a=3, b=4, mid={'i_start': 0})
    add(rst=1, start=0, en=1, mode=0, a=3, b=4, mid={'i_mode': 1})
    add(rst=1, start=0, en=1, mode=0, a=3, b=4)

    # Random exploration
    while len(rows) < cycles:
        rst = 1 if rng.random() > 0.03 else 0
        en = 1 if rng.random() > 0.1 else 0
        start = 1 if rng.random() > 0.5 else 0
        mode = rng.randint(0, 1)
        clr = 1 if rng.random() > 0.92 else 0
        a = rng.randint(0, 255)
        b = rng.randint(0, 255)
        mid = None
        if rng.random() > 0.85:
            mid = {}
            if rng.random() > 0.5:
                mid['i_start'] = rng.randint(0, 1)
            if rng.random() > 0.5:
                mid['i_mode'] = rng.randint(0, 1)
            if rng.random() > 0.7:
                mid['i_operand_a'] = rng.randint(0, 255)
            if rng.random() > 0.7:
                mid['i_operand_b'] = rng.randint(0, 255)
        add(rst=rst, start=start, en=en, mode=mode, clr=clr, a=a, b=b, mid=mid)

    return rows[:cycles]

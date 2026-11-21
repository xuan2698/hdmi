def stimulus(rng, cycles):
    rows = []
    def u16(v):
        return v & 0xFFFF

    for _ in range(4):
        rows.append({'reset': 1, 'in_1': 0, 'in_2': 0, 'in_3': 0, 'filter_select': 0})

    n = cycles - 4
    pattern = []

    for i in range(60):
        if i == 0:
            pattern.append((0x7FFF, 0x8000, 0x0001, 0))
        elif i < 8:
            pattern.append((0, 0, 0, 0))
        elif i < 20:
            pattern.append((0x1000, 0x2000, 0x3000, 0))
        elif i < 40:
            v = (i * 0x0800) & 0xFFFF
            pattern.append((v, (0xFFFF - v) & 0xFFFF, (v * 3) & 0xFFFF, 0))
        else:
            pattern.append((rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), 0))

    for i in range(60):
        v = (i * 0x0400) & 0xFFFF
        if i % 2 == 0:
            pattern.append((v, (0xFFFF - v) & 0xFFFF, (v * 2) & 0xFFFF, 1))
        else:
            pattern.append(((0xFFFF - v) & 0xFFFF, v, (0x8000 + v) & 0xFFFF, 1))

    for i in range(60):
        if i % 10 == 0:
            pattern.append((0x8000, 0x7FFF, 0xFFFF, 2))
        elif i % 10 == 5:
            pattern.append((0x0000, 0xFFFF, 0x0000, 2))
        else:
            pattern.append((rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), 2))

    for i in range(40):
        pattern.append((rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), 3))

    remaining = n - len(pattern)
    if remaining > 0:
        run_len = min(remaining, 120)
        for _ in range(run_len):
            pattern.append((0x1234, 0x5678, 0x9ABC, 0))
        remaining -= run_len
    if remaining > 0:
        run_len = min(remaining, 120)
        for _ in range(run_len):
            pattern.append((0xFFFF, 0x0000, 0x8000, 1))
        remaining -= run_len
    if remaining > 0:
        run_len = min(remaining, 120)
        for _ in range(run_len):
            pattern.append((0x0001, 0x0002, 0x0003, 2))
        remaining -= run_len
    if remaining > 0:
        fs = 0
        for i in range(remaining):
            if i % 37 == 0:
                fs = rng.randint(0, 3)
            pattern.append((rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), fs))

    if len(pattern) > n:
        pattern = pattern[:n]
    while len(pattern) < n:
        pattern.append((rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), rng.randint(0, 3)))

    for i in range(n):
        in1, in2, in3, fs = pattern[i]
        row = {
            'reset': 0,
            'in_1': u16(in1),
            'in_2': u16(in2),
            'in_3': u16(in3),
            'filter_select': fs & 0x3,
        }
        if i % 29 == 0 and i > 0:
            row['mid'] = {
                'in_1': rng.randint(0, 0xFFFF),
                'in_2': rng.randint(0, 0xFFFF),
                'in_3': rng.randint(0, 0xFFFF),
                'filter_select': rng.randint(0, 3),
            }
        rows.append(row)

    return rows

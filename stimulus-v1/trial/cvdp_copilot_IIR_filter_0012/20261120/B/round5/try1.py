def stimulus(rng, cycles):
    rows = []
    def u(v, w):
        return v & ((1 << w) - 1)

    reset_len = 6
    for i in range(reset_len):
        rows.append({'reset': 1, 'in_1': 0, 'in_2': 0, 'in_3': 0, 'filter_select': 0})

    n = cycles - reset_len
    pattern = []

    # Butterworth: impulse response, then step, then zeros
    for i in range(60):
        if i == 0:
            pattern.append((0x7FFF, 0x8000, 0x0001, 0))
        elif i < 12:
            pattern.append((0x0000, 0x0000, 0x0000, 0))
        elif i < 30:
            pattern.append((0x1000, 0x2000, 0x3000, 0))
        else:
            pattern.append((rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), 0))

    # Chebyshev: ramp up and down
    for i in range(60):
        v = (i * 0x0400) & 0xFFFF
        pattern.append((v, (0xFFFF - v) & 0xFFFF, (v * 2) & 0xFFFF, 1))

    # Elliptic: random
    for i in range(60):
        pattern.append((rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), 2))

    # Default filter_select=3
    for i in range(40):
        pattern.append((rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), 3))

    remaining = n - len(pattern)
    if remaining > 0:
        run_len = min(remaining, 120)
        for i in range(run_len):
            pattern.append((0x1234, 0x5678, 0x9ABC, 0))
        remaining -= run_len
        run_len = min(remaining, 120)
        for i in range(run_len):
            pattern.append((0xFFFF, 0x0000, 0x8000, 1))
        remaining -= run_len
        run_len = min(remaining, 80)
        for i in range(run_len):
            pattern.append((0x0000, 0xFFFF, 0x7FFF, 2))
        remaining -= run_len
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
            'in_1': in1 & 0xFFFF,
            'in_2': in2 & 0xFFFF,
            'in_3': in3 & 0xFFFF,
            'filter_select': fs & 0x3,
        }
        if i % 23 == 0 and i > 0:
            row['mid'] = {
                'in_1': rng.randint(0, 0xFFFF),
                'in_2': rng.randint(0, 0xFFFF),
                'in_3': rng.randint(0, 0xFFFF),
                'filter_select': rng.randint(0, 3),
            }
        rows.append(row)

    return rows

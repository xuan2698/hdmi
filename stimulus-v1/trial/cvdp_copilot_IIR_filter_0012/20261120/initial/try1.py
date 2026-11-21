def stimulus(rng, cycles):
    rows = []
    def u(v, w):
        return v & ((1 << w) - 1)
    def s16(v):
        v &= 0xFFFF
        return v - 0x10000 if v >= 0x8000 else v
    def to_u16(v):
        return v & 0xFFFF

    # Reset sequence: hold reset high for a few cycles
    reset_len = 4
    for i in range(reset_len):
        rows.append({
            'reset': 1,
            'in_1': 0, 'in_2': 0, 'in_3': 0,
            'filter_select': 0,
        })

    # After reset, generate stimulus
    # Track filter select phases to exercise all modes
    # Also generate impulse, step, ramp, and random patterns
    n = cycles - reset_len
    # Phase plan (in cycles):
    # 0-49: Butterworth with impulse/step
    # 50-99: Chebyshev with ramp
    # 100-149: Elliptic with random
    # 150-199: filter_select=3 (default) with random
    # 200+: mixed random with occasional filter changes
    # We'll build a list of (in1,in2,in3,fs) tuples

    # Precompute a pattern list
    pattern = []
    # Butterworth phase: impulse then step then small random
    for i in range(50):
        if i == 0:
            pattern.append((0x7FFF, 0x8000, 0x0001, 0))
        elif i < 10:
            pattern.append((0x0000, 0x0000, 0x0000, 0))
        elif i < 20:
            pattern.append((0x1000, 0x2000, 0x3000, 0))
        else:
            pattern.append((rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), 0))
    # Chebyshev phase: ramp
    for i in range(50):
        v = (i * 0x0400) & 0xFFFF
        pattern.append((v, (0xFFFF - v) & 0xFFFF, (v * 2) & 0xFFFF, 1))
    # Elliptic phase: random
    for i in range(50):
        pattern.append((rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), 2))
    # Default filter_select=3 phase
    for i in range(50):
        pattern.append((rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), 3))
    # Remaining: mixed with occasional filter changes and long runs
    remaining = n - len(pattern)
    if remaining > 0:
        # Long run of constant values with filter 0
        run_len = min(remaining, 100)
        for i in range(run_len):
            pattern.append((0x1234, 0x5678, 0x9ABC, 0))
        remaining -= run_len
        # Long run with filter 1
        run_len = min(remaining, 100)
        for i in range(run_len):
            pattern.append((0xFFFF, 0x0000, 0x8000, 1))
        remaining -= run_len
        # Random remainder with occasional filter changes
        fs = 0
        for i in range(remaining):
            if i % 37 == 0:
                fs = rng.randint(0, 3)
            pattern.append((rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), fs))

    # Trim or pad pattern to exactly n
    if len(pattern) > n:
        pattern = pattern[:n]
    while len(pattern) < n:
        pattern.append((rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), rng.randint(0, 0xFFFF), rng.randint(0, 3)))

    # Build rows with optional mid overrides
    for i in range(n):
        in1, in2, in3, fs = pattern[i]
        row = {
            'reset': 0,
            'in_1': in1 & 0xFFFF,
            'in_2': in2 & 0xFFFF,
            'in_3': in3 & 0xFFFF,
            'filter_select': fs & 0x3,
        }
        # Occasionally add mid overrides to exercise post-rising-edge changes
        if i % 23 == 0 and i > 0:
            row['mid'] = {
                'in_1': rng.randint(0, 0xFFFF),
                'in_2': rng.randint(0, 0xFFFF),
                'in_3': rng.randint(0, 0xFFFF),
                'filter_select': rng.randint(0, 3),
            }
        rows.append(row)

    return rows

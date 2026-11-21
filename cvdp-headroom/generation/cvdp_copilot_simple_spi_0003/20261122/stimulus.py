def stimulus(rng, cycles):
    rows = []
    # Phase plan (indices into rows):
    # 0-3 reset low, 4-... reset high
    # We'll build a sequence of (enable, fault, clear, data) tuples with optional mid changes.
    seq = []
    # Reset phase
    for _ in range(4):
        seq.append((0, 0, 0, 0, None))
    # Idle with enable low
    for _ in range(3):
        seq.append((0, 0, 0, rng.randrange(1 << 16), None))
    # Normal transmission: enable high, various data
    data_patterns = [0x0000, 0xFFFF, 0x8000, 0x0001, 0xAAAA, 0x5555,
                     0x1234, 0xF0F0, 0x00FF, 0xFF00, 0x0002, 0x4000]
    for d in data_patterns:
        seq.append((1, 0, 0, d, None))
        # hold enable for a while to let transmission proceed
        for _ in range(rng.randrange(20, 40)):
            seq.append((1, 0, 0, rng.randrange(1 << 16), None))
    # Disable mid-transmission
    seq.append((1, 0, 0, 0xABCD, None))
    for _ in range(5):
        seq.append((1, 0, 0, 0x1111, None))
    seq.append((0, 0, 0, 0x2222, None))
    for _ in range(5):
        seq.append((0, 0, 0, 0x3333, None))
    # Re-enable
    for _ in range(30):
        seq.append((1, 0, 0, 0x4444, None))
    # Clear mid-transmission
    seq.append((1, 0, 0, 0x5555, None))
    for _ in range(3):
        seq.append((1, 0, 0, 0x6666, None))
    seq.append((1, 0, 1, 0x7777, None))
    seq.append((1, 0, 0, 0x8888, None))
    for _ in range(20):
        seq.append((1, 0, 0, 0x9999, None))
    # Fault during transmission
    seq.append((1, 0, 0, 0xAAAA, None))
    for _ in range(3):
        seq.append((1, 0, 0, 0xBBBB, None))
    seq.append((1, 1, 0, 0xCCCC, None))
    for _ in range(5):
        seq.append((1, 1, 0, 0xDDDD, None))
    # Recover via clear
    seq.append((1, 1, 1, 0xEEEE, None))
    seq.append((1, 0, 0, 0xFFFF, None))
    for _ in range(20):
        seq.append((1, 0, 0, rng.randrange(1 << 16), None))
    # Fault while idle
    seq.append((0, 1, 0, 0x1234, None))
    for _ in range(3):
        seq.append((0, 1, 0, 0x5678, None))
    seq.append((0, 1, 1, 0x9ABC, None))
    seq.append((0, 0, 0, 0xDEF0, None))
    # Back-to-back transmissions with mid changes
    for _ in range(10):
        d = rng.randrange(1 << 16)
        seq.append((1, 0, 0, d, {'i_data_in': rng.randrange(1 << 16)}))
        for _ in range(rng.randrange(15, 35)):
            seq.append((1, 0, 0, rng.randrange(1 << 16), None))
    # Random exploration
    while len(seq) < cycles:
        en = rng.randrange(2)
        fl = 1 if rng.random() < 0.05 else 0
        cl = 1 if rng.random() < 0.05 else 0
        d = rng.randrange(1 << 16)
        mid = None
        if rng.random() < 0.1:
            mid = {'i_data_in': rng.randrange(1 << 16)}
        seq.append((en, fl, cl, d, mid))
    # Trim/pad to exactly cycles
    seq = seq[:cycles]
    while len(seq) < cycles:
        seq.append((0, 0, 0, 0, None))
    for (en, fl, cl, d, mid) in seq:
        row = {'i_rst_b': 1, 'i_data_in': d & 0xFFFF,
               'i_enable': en, 'i_fault': fl, 'i_clear': cl}
        if mid is not None:
            row['mid'] = dict(mid)
        rows.append(row)
    # First few rows reset low
    for i in range(4):
        rows[i]['i_rst_b'] = 0
    return rows

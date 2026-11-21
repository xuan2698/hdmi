def stimulus(rng, cycles):
    rows = []
    def u(v, w):
        return v & ((1 << w) - 1)
    for _ in range(4):
        rows.append({'reset': 1, 'in_1': 0, 'in_2': 0, 'in_3': 0, 'filter_select': 0})
    modes = [0, 1, 2, 3]
    mode_idx = 0
    run_len = 0
    cur_mode = 0
    while len(rows) < cycles:
        if run_len <= 0:
            cur_mode = modes[mode_idx % 4]
            mode_idx += 1
            run_len = rng.randint(20, 80)
        run_len -= 1
        r = rng.random()
        if r < 0.08:
            v1 = 0
            v2 = 0
            v3 = 0
        elif r < 0.16:
            v1 = u(0x7FFF, 16)
            v2 = u(0x8000, 16)
            v3 = u(0xFFFF, 16)
        elif r < 0.24:
            v1 = u(rng.randint(0, 0xFF), 16)
            v2 = u(rng.randint(0, 0xFF), 16)
            v3 = u(rng.randint(0, 0xFF), 16)
        elif r < 0.34:
            v1 = u(rng.randint(0x7F00, 0x80FF), 16)
            v2 = u(rng.randint(0x7F00, 0x80FF), 16)
            v3 = u(rng.randint(0x7F00, 0x80FF), 16)
        elif r < 0.46:
            v1 = u(rng.randint(0, 0xFFFF), 16)
            v2 = u(rng.randint(0, 0xFFFF), 16)
            v3 = u(rng.randint(0, 0xFFFF), 16)
        elif r < 0.56:
            v1 = u(0x0001, 16)
            v2 = u(0x0002, 16)
            v3 = u(0x0003, 16)
        elif r < 0.66:
            v1 = u(0xFFFE, 16)
            v2 = u(0xFFFD, 16)
            v3 = u(0xFFFC, 16)
        elif r < 0.76:
            v1 = u(0x0000, 16)
            v2 = u(0xFFFF, 16)
            v3 = u(0x0001, 16)
        elif r < 0.86:
            v1 = u(0x8000, 16)
            v2 = u(0x7FFF, 16)
            v3 = u(0x8000, 16)
        else:
            v1 = u(rng.randint(0, 0xFFFF), 16)
            v2 = u(rng.randint(0, 0xFFFF), 16)
            v3 = u(rng.randint(0, 0xFFFF), 16)
        row = {'reset': 0, 'in_1': v1, 'in_2': v2, 'in_3': v3, 'filter_select': cur_mode}
        if rng.random() < 0.12:
            row['mid'] = {
                'in_1': u(rng.randint(0, 0xFFFF), 16),
                'in_2': u(rng.randint(0, 0xFFFF), 16),
                'in_3': u(rng.randint(0, 0xFFFF), 16),
                'filter_select': rng.randint(0, 3),
            }
        rows.append(row)
    return rows[:cycles]

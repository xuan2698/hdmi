def stimulus(rng, cycles):
    rows = []
    def u(v, w):
        return v & ((1 << w) - 1)
    # reset sequence
    for _ in range(4):
        rows.append({'reset': 1, 'in_1': 0, 'in_2': 0, 'in_3': 0, 'filter_select': 0})
    modes = [0, 1, 2, 3]
    mode_idx = 0
    run_len = 0
    cur_mode = 0
    phase = 0
    while len(rows) < cycles:
        if run_len <= 0:
            cur_mode = modes[mode_idx % 4]
            mode_idx += 1
            run_len = rng.randint(8, 40)
            phase = 0
        run_len -= 1
        phase += 1
        if phase == 1:
            v1, v2, v3 = u(0x7FFF, 16), u(0x8000, 16), u(0xFFFF, 16)
        elif phase == 2:
            v1, v2, v3 = 0, 0, 0
        elif phase == 3:
            v1, v2, v3 = u(0x0001, 16), u(0x0002, 16), u(0x0003, 16)
        elif phase <= 6:
            v1, v2, v3 = 0, 0, 0
        else:
            r = rng.random()
            if r < 0.12:
                v1 = v2 = v3 = 0
            elif r < 0.24:
                v1, v2, v3 = u(0x7FFF, 16), u(0x8000, 16), u(0xFFFF, 16)
            elif r < 0.36:
                v1 = u(rng.randint(0, 0xFF), 16)
                v2 = u(rng.randint(0, 0xFF), 16)
                v3 = u(rng.randint(0, 0xFF), 16)
            elif r < 0.50:
                v1 = u(rng.randint(0, 0xFFFF), 16)
                v2 = u(rng.randint(0, 0xFFFF), 16)
                v3 = u(rng.randint(0, 0xFFFF), 16)
            elif r < 0.65:
                v1 = u(rng.randint(0x7F00, 0x80FF), 16)
                v2 = u(rng.randint(0x7F00, 0x80FF), 16)
                v3 = u(rng.randint(0x7F00, 0x80FF), 16)
            elif r < 0.80:
                v1 = u(rng.randint(0, 0xFFFF), 16)
                v2 = u(rng.randint(0, 0xFFFF), 16)
                v3 = u(rng.randint(0, 0xFFFF), 16)
            else:
                v1 = u(rng.randint(0, 0xFFFF), 16)
                v2 = u(rng.randint(0, 0xFFFF), 16)
                v3 = u(rng.randint(0, 0xFFFF), 16)
        row = {'reset': 0, 'in_1': v1, 'in_2': v2, 'in_3': v3, 'filter_select': cur_mode}
        if rng.random() < 0.08:
            row['mid'] = {
                'in_1': u(rng.randint(0, 0xFFFF), 16),
                'in_2': u(rng.randint(0, 0xFFFF), 16),
                'in_3': u(rng.randint(0, 0xFFFF), 16),
                'filter_select': rng.randint(0, 3),
            }
        rows.append(row)
    return rows[:cycles]

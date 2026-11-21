def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        if i < 4:
            rst = 1
            data_in = 0
            has_data = 0
        elif i < 8:
            rst = 0
            data_in = 0
            has_data = 0
        else:
            rst = 0
            phase = (i - 8) % 48
            if phase < 3:
                has_data = 1
                data_in = rng.randint(0, 15)
            elif phase < 6:
                has_data = 0
                data_in = rng.randint(0, 15)
            elif phase < 10:
                has_data = 1
                data_in = (i * 3 + 1) & 0xF
            elif phase < 14:
                has_data = 0
                data_in = 0
            elif phase < 18:
                has_data = 1
                data_in = rng.randint(0, 15)
            elif phase < 22:
                has_data = 1
                data_in = (i ^ 0x5) & 0xF
            elif phase < 26:
                has_data = 0
                data_in = rng.randint(0, 15)
            elif phase < 30:
                has_data = 1
                data_in = (i * 7 + 2) & 0xF
            elif phase < 34:
                has_data = 0
                data_in = 0
            elif phase < 38:
                has_data = 1
                data_in = rng.randint(0, 15)
            elif phase < 42:
                has_data = 1
                data_in = (i * 11) & 0xF
            else:
                has_data = 0
                data_in = rng.randint(0, 15)
        row = {
            'rst': rst & 0x1,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data & 0x1,
        }
        rows.append(row)
    return rows

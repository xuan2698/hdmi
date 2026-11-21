def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        if i < 3:
            rst = 1
            data_in = 0
            has_data = 0
        elif i < 6:
            rst = 0
            data_in = 0
            has_data = 0
        else:
            rst = 0
            phase = (i - 6) % 64
            if phase < 2:
                has_data = 1
                data_in = rng.randint(0, 15)
            elif phase < 5:
                has_data = 0
                data_in = rng.randint(0, 15)
            elif phase < 9:
                has_data = 1
                data_in = (i * 3 + 1) & 0xF
            elif phase < 13:
                has_data = 0
                data_in = 0
            elif phase < 17:
                has_data = 1
                data_in = rng.randint(0, 15)
            elif phase < 21:
                has_data = 1
                data_in = (i ^ 0x5) & 0xF
            elif phase < 25:
                has_data = 0
                data_in = rng.randint(0, 15)
            elif phase < 29:
                has_data = 1
                data_in = (i * 7 + 2) & 0xF
            elif phase < 33:
                has_data = 0
                data_in = 0
            elif phase < 37:
                has_data = 1
                data_in = rng.randint(0, 15)
            elif phase < 41:
                has_data = 1
                data_in = (i * 11) & 0xF
            elif phase < 45:
                has_data = 0
                data_in = rng.randint(0, 15)
            elif phase < 49:
                has_data = 1
                data_in = (i * 13 + 5) & 0xF
            elif phase < 53:
                has_data = 0
                data_in = rng.randint(0, 15)
            elif phase < 57:
                has_data = 1
                data_in = (i * 17 + 3) & 0xF
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

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
            phase = (i - 6) % 40
            if phase < 4:
                has_data = 1
                data_in = rng.randint(0, 15)
            elif phase < 8:
                has_data = 0
                data_in = rng.randint(0, 15)
            elif phase < 12:
                has_data = 1
                data_in = (i * 5 + 3) & 0xF
            elif phase < 16:
                has_data = 0
                data_in = 0
            elif phase < 20:
                has_data = 1
                data_in = rng.randint(0, 15)
            elif phase < 24:
                has_data = 1
                data_in = (i ^ 0xA) & 0xF
            elif phase < 28:
                has_data = 0
                data_in = rng.randint(0, 15)
            elif phase < 32:
                has_data = 1
                data_in = (i * 7) & 0xF
            elif phase < 36:
                has_data = 0
                data_in = 0
            else:
                has_data = 1
                data_in = rng.randint(0, 15)
        row = {
            'rst': rst & 0x1,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data & 0x1,
        }
        rows.append(row)
    return rows

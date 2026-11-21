def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        if i < 4:
            rst = 1
            data_in = 0
            has_data = 0
        else:
            rst = 0
            phase = (i - 4) % 16
            if phase < 4:
                has_data = 1
                data_in = rng.randint(0, 15)
            elif phase < 8:
                has_data = 0
                data_in = rng.randint(0, 15)
            elif phase < 12:
                has_data = 1
                data_in = (i * 3 + 5) & 0xF
            else:
                has_data = 0
                data_in = 0
            if rng.random() < 0.05:
                rst = 1
                data_in = 0
                has_data = 0
        row = {
            'rst': rst & 0x1,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data & 0x1,
        }
        rows.append(row)
    return rows

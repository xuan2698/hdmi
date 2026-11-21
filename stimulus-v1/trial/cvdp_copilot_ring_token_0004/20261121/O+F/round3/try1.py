def stimulus(rng, cycles):
    rows = []
    rst = 1
    data_in = 0
    has_data_to_send = 0
    for i in range(cycles):
        if i < 2:
            rst = 1
            data_in = 0
            has_data_to_send = 0
        elif i < 4:
            rst = 0
            data_in = 0
            has_data_to_send = 0
        else:
            rst = 0
            phase = (i - 4) % 24
            if phase < 4:
                has_data_to_send = 1
                data_in = (i * 3 + 1) & 0xF
            elif phase < 8:
                has_data_to_send = 0
                data_in = (i * 5 + 2) & 0xF
            elif phase < 12:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            elif phase < 16:
                has_data_to_send = 0
                data_in = 0
            elif phase < 20:
                has_data_to_send = 1
                data_in = (i * 7 + 3) & 0xF
            else:
                has_data_to_send = 0
                data_in = rng.randrange(16)
        row = {
            'rst': rst & 0x1,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data_to_send & 0x1,
        }
        rows.append(row)
    return rows

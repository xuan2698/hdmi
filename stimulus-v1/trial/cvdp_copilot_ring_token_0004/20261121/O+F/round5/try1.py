def stimulus(rng, cycles):
    rows = []
    rst = 1
    data_in = 0
    has_data_to_send = 0
    for i in range(cycles):
        if i < 3:
            rst = 1
            data_in = 0
            has_data_to_send = 0
        elif i < 6:
            rst = 0
            data_in = 0
            has_data_to_send = 0
        else:
            rst = 0
            phase = (i - 6) % 40
            if phase < 5:
                has_data_to_send = 1
                data_in = (i * 3 + 1) & 0xF
            elif phase < 10:
                has_data_to_send = 0
                data_in = (i * 5 + 2) & 0xF
            elif phase < 15:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            elif phase < 20:
                has_data_to_send = 0
                data_in = 0
            elif phase < 25:
                has_data_to_send = 1
                data_in = (i * 7 + 3) & 0xF
            elif phase < 30:
                has_data_to_send = 0
                data_in = rng.randrange(16)
            elif phase < 35:
                has_data_to_send = 1
                data_in = (i * 11 + 5) & 0xF
            else:
                has_data_to_send = 0
                data_in = (i * 13 + 7) & 0xF
        row = {
            'rst': rst & 0x1,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data_to_send & 0x1,
        }
        rows.append(row)
    return rows

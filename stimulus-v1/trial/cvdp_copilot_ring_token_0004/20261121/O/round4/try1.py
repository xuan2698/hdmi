def stimulus(rng, cycles):
    rows = []
    rst = 1
    data_in = 0
    has_data_to_send = 0
    for i in range(cycles):
        if i < 4:
            rst = 1
            data_in = 0
            has_data_to_send = 0
        elif i < 8:
            rst = 0
            data_in = 0
            has_data_to_send = 0
        else:
            rst = 0
            phase = (i - 8) % 24
            if phase < 6:
                has_data_to_send = 1
                data_in = (i * 5 + 3) & 0xF
            elif phase < 12:
                has_data_to_send = 0
                data_in = (i * 11 + 7) & 0xF
            elif phase < 18:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            else:
                has_data_to_send = 0
                data_in = 0
            if rng.random() < 0.10:
                has_data_to_send = 1 - has_data_to_send
            if rng.random() < 0.06:
                data_in = rng.randrange(16)
            if rng.random() < 0.03:
                rst = 1
                data_in = 0
                has_data_to_send = 0
        row = {
            'rst': rst & 0x1,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data_to_send & 0x1,
        }
        rows.append(row)
    return rows

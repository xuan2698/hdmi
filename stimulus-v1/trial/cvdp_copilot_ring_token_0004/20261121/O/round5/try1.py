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
            phase = (i - 6) % 32
            if phase < 8:
                has_data_to_send = 1
                data_in = (i * 3 + 5) & 0xF
            elif phase < 16:
                has_data_to_send = 0
                data_in = (i * 7 + 1) & 0xF
            elif phase < 24:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            else:
                has_data_to_send = 0
                data_in = 0
            if rng.random() < 0.12:
                has_data_to_send = 1 - has_data_to_send
            if rng.random() < 0.08:
                data_in = rng.randrange(16)
            if rng.random() < 0.02:
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

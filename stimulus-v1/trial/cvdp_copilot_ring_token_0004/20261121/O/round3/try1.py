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
            phase = (i - 6) % 20
            if phase < 5:
                has_data_to_send = 1
                data_in = (i * 3 + 5) & 0xF
            elif phase < 10:
                has_data_to_send = 0
                data_in = (i * 7 + 2) & 0xF
            elif phase < 15:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            else:
                has_data_to_send = 0
                data_in = 0
            if rng.random() < 0.08:
                has_data_to_send = 1 - has_data_to_send
            if rng.random() < 0.05:
                data_in = rng.randrange(16)
        row = {
            'rst': rst & 0x1,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data_to_send & 0x1,
        }
        rows.append(row)
    return rows

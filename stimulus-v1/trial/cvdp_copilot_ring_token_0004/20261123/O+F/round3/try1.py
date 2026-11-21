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
        elif i < 12:
            rst = 0
            data_in = (i * 3) & 0xF
            has_data_to_send = 1
        elif i < 20:
            rst = 0
            data_in = (i * 5) & 0xF
            has_data_to_send = 0
        elif i < 40:
            rst = 0
            data_in = (i * 7) & 0xF
            has_data_to_send = 1
        else:
            rst = 0
            r = rng.random()
            if r < 0.10:
                data_in = rng.randrange(16)
            elif r < 0.20:
                data_in = (data_in + 1) & 0xF
            elif r < 0.28:
                data_in = (data_in << 1) & 0xF
            elif r < 0.34:
                data_in = (data_in ^ 0xA) & 0xF
            if rng.random() < 0.35:
                has_data_to_send = 1 - has_data_to_send
            if rng.random() < 0.12:
                has_data_to_send = 1
            if rng.random() < 0.08:
                has_data_to_send = 0
            if rng.random() < 0.02:
                rst = 1
                data_in = 0
                has_data_to_send = 0
        row = {
            'rst': rst & 0x1,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data_to_send & 0x1,
        }
        if rng.random() < 0.30:
            mid_data = data_in
            mid_send = has_data_to_send
            if rng.random() < 0.6:
                mid_data = rng.randrange(16)
            if rng.random() < 0.6:
                mid_send = rng.randrange(2)
            row['mid'] = {'data_in': mid_data & 0xF, 'has_data_to_send': mid_send & 0x1}
        rows.append(row)
    return rows

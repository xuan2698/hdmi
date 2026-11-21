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
        elif i < 10:
            rst = 0
            data_in = (i * 2 + 1) & 0xF
            has_data_to_send = 1
        elif i < 20:
            rst = 0
            data_in = (data_in + 3) & 0xF
            has_data_to_send = 0
        elif i < 30:
            rst = 0
            data_in = (data_in ^ 0x5) & 0xF
            has_data_to_send = 1
        elif i < 45:
            rst = 0
            data_in = (data_in + 7) & 0xF
            has_data_to_send = (i & 1)
        elif i < 60:
            rst = 0
            data_in = (data_in - 2) & 0xF
            has_data_to_send = 1
        else:
            rst = 0
            r = rng.random()
            if r < 0.20:
                data_in = rng.randrange(16)
            elif r < 0.40:
                data_in = (data_in + 1) & 0xF
            elif r < 0.55:
                data_in = (data_in - 1) & 0xF
            elif r < 0.70:
                data_in = (data_in ^ 0xF) & 0xF
            elif r < 0.85:
                data_in = (data_in + 4) & 0xF
            if rng.random() < 0.40:
                has_data_to_send = 1 - has_data_to_send
            if rng.random() < 0.20:
                has_data_to_send = 1
            if rng.random() < 0.15:
                has_data_to_send = 0
            if rng.random() < 0.015:
                rst = 1
                data_in = 0
                has_data_to_send = 0
        row = {
            'rst': rst & 0x1,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data_to_send & 0x1,
        }
        if rng.random() < 0.35:
            mid_data = data_in
            mid_send = has_data_to_send
            if rng.random() < 0.6:
                mid_data = rng.randrange(16)
            if rng.random() < 0.6:
                mid_send = rng.randrange(2)
            row['mid'] = {'data_in': mid_data & 0xF, 'has_data_to_send': mid_send & 0x1}
        rows.append(row)
    return rows

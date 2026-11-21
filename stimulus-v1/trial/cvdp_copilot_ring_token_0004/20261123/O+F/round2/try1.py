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
        elif i == 2:
            rst = 0
            data_in = 8
            has_data_to_send = 1
        elif i == 3:
            rst = 0
            data_in = 4
            has_data_to_send = 1
        elif i == 4:
            rst = 0
            data_in = 12
            has_data_to_send = 1
        elif i == 5:
            rst = 0
            data_in = 2
            has_data_to_send = 1
        else:
            rst = 0
            r = rng.random()
            if r < 0.12:
                data_in = rng.randrange(16)
            elif r < 0.22:
                data_in = (data_in + 1) & 0xF
            elif r < 0.30:
                data_in = (data_in << 1) & 0xF
            if rng.random() < 0.30:
                has_data_to_send = 1 - has_data_to_send
            if rng.random() < 0.10:
                has_data_to_send = 1
            if rng.random() < 0.06:
                has_data_to_send = 0
            if rng.random() < 0.03:
                rst = 1
                data_in = 0
                has_data_to_send = 0
        row = {
            'rst': rst & 0x1,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data_to_send & 0x1,
        }
        if rng.random() < 0.25:
            mid_data = data_in
            mid_send = has_data_to_send
            if rng.random() < 0.5:
                mid_data = rng.randrange(16)
            if rng.random() < 0.5:
                mid_send = rng.randrange(2)
            row['mid'] = {'data_in': mid_data & 0xF, 'has_data_to_send': mid_send & 0x1}
        rows.append(row)
    return rows

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
        elif i == 3:
            rst = 0
            data_in = rng.randrange(16)
            has_data_to_send = rng.randrange(2)
        else:
            rst = 0
            r = rng.random()
            if r < 0.15:
                data_in = rng.randrange(16)
            elif r < 0.25:
                data_in = (data_in + 1) & 0xF
            if rng.random() < 0.35:
                has_data_to_send = 1 - has_data_to_send
            if rng.random() < 0.08:
                has_data_to_send = 1
            if rng.random() < 0.05:
                has_data_to_send = 0
        row = {
            'rst': rst,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data_to_send & 0x1,
        }
        if rng.random() < 0.3:
            mid_data = data_in
            mid_send = has_data_to_send
            if rng.random() < 0.5:
                mid_data = rng.randrange(16)
            if rng.random() < 0.5:
                mid_send = rng.randrange(2)
            row['mid'] = {'data_in': mid_data & 0xF, 'has_data_to_send': mid_send & 0x1}
        rows.append(row)
    return rows

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
            r = rng.random()
            if r < 0.20:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            elif r < 0.30:
                has_data_to_send = 0
                data_in = rng.randrange(16)
            elif r < 0.40:
                has_data_to_send = 1
                data_in = data_in
            elif r < 0.50:
                has_data_to_send = 0
                data_in = 0
            elif r < 0.60:
                has_data_to_send = 1
                data_in = 0
            elif r < 0.70:
                has_data_to_send = 0
                data_in = 15
            elif r < 0.80:
                has_data_to_send = 1
                data_in = 15
            else:
                has_data_to_send = 0
                data_in = 0
        row = {
            'rst': rst & 0x1,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data_to_send & 0x1,
        }
        rows.append(row)
    return rows

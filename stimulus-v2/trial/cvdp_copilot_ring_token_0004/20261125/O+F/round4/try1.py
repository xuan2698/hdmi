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
        elif i < 6:
            rst = 0
            data_in = (i * 3) & 0xF
            has_data_to_send = 1
        elif i < 10:
            rst = 0
            data_in = (i * 5 + 1) & 0xF
            has_data_to_send = 1
        else:
            rst = 0
            r = rng.random()
            if r < 0.12:
                data_in = 0
                has_data_to_send = 0
            elif r < 0.50:
                data_in = rng.randrange(16)
                has_data_to_send = 1
            else:
                data_in = rng.randrange(16)
                has_data_to_send = 0
        row = {
            'rst': rst & 1,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data_to_send & 1,
        }
        rows.append(row)
    return rows

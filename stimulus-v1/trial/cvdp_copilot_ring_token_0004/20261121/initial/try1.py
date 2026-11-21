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
            r = rng.random()
            if r < 0.15:
                has_data_to_send = 1
                data_in = rng.randrange(16)
            elif r < 0.25:
                has_data_to_send = 0
                data_in = rng.randrange(16)
            elif r < 0.35:
                has_data_to_send = 1
                data_in = data_in
            else:
                has_data_to_send = 0
                data_in = 0
        row = {
            'rst': rst,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data_to_send & 0x1,
        }
        rows.append(row)
    return rows

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
        else:
            rst = 0
            if i < 8:
                data_in = rng.randrange(16)
                has_data_to_send = 1
            elif i < 20:
                data_in = rng.randrange(16)
                has_data_to_send = 0
            elif i < 40:
                data_in = rng.randrange(16)
                has_data_to_send = 1
            elif i < 60:
                data_in = rng.randrange(16)
                has_data_to_send = 0
            else:
                data_in = rng.randrange(16)
                has_data_to_send = 1 if rng.random() < 0.5 else 0
        row = {
            'rst': rst,
            'data_in': data_in,
            'has_data_to_send': has_data_to_send,
        }
        rows.append(row)
    return rows

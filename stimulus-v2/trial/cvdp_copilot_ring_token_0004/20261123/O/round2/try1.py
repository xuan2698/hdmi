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
            if i == 3:
                data_in = rng.randrange(16)
                has_data_to_send = rng.randrange(2)
            else:
                if rng.random() < 0.35:
                    data_in = rng.randrange(16)
                if rng.random() < 0.30:
                    has_data_to_send = rng.randrange(2)
        rows.append({
            'rst': rst & 0x1,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data_to_send & 0x1,
        })
    return rows

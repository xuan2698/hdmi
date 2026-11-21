def stimulus(rng, cycles):
    rows = []
    rst = 1
    data_in = 0
    has_data_to_send = 0
    for i in range(4000):
        if i == 3:
            rst = 0
        if i > 3:
            if rng.random() < 0.15:
                data_in = rng.randrange(16)
            if rng.random() < 0.4:
                has_data_to_send = rng.randrange(2)
        row = {
            'rst': rst,
            'data_in': data_in,
            'has_data_to_send': has_data_to_send,
        }
        rows.append(row)
    return rows

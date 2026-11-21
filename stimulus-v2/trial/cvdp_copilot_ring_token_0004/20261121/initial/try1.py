def stimulus(rng, cycles):
    rows = []
    rst = 1
    data_in = 0
    has_data_to_send = 0
    for i in range(cycles):
        if i == 3:
            rst = 0
        if rst == 0:
            data_in = rng.randrange(16)
            has_data_to_send = 1 if rng.random() < 0.4 else 0
        rows.append({
            'rst': rst,
            'data_in': data_in,
            'has_data_to_send': has_data_to_send,
        })
    return rows

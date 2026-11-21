def stimulus(rng, cycles):
    rows = []
    rst = 1
    data_in = 0
    has_data_to_send = 0
    for i in range(cycles):
        if i < 3:
            rst = 1
        else:
            rst = 0
        if i >= 3:
            if i % 7 == 0:
                data_in = rng.randrange(16)
            if i % 5 == 0:
                has_data_to_send = rng.randrange(2)
            elif i % 11 == 0:
                has_data_to_send = 1
        rows.append({
            'rst': rst,
            'data_in': data_in,
            'has_data_to_send': has_data_to_send,
        })
    return rows

def stimulus(rng, cycles):
    rows = []
    state = 0
    for i in range(cycles):
        if i < 3:
            rst = 1
            data_in = 0
            has_data = 0
        else:
            rst = 0
            r = rng.random()
            if r < 0.15:
                has_data = 1
                data_in = rng.randint(0, 15)
            elif r < 0.25:
                has_data = 0
                data_in = rng.randint(0, 15)
            else:
                has_data = 0
                data_in = 0
        row = {
            'rst': rst,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data & 0x1,
        }
        rows.append(row)
    return rows

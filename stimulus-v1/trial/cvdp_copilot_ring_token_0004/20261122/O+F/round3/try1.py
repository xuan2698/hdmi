def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        if i < 2:
            rst = 1
            data_in = 0
            has_data = 0
        elif i < 6:
            rst = 0
            has_data = 1
            data_in = (i * 3 + 1) & 0xF
        elif i < 10:
            rst = 0
            has_data = 0
            data_in = 0
        else:
            rst = 0
            r = rng.random()
            if r < 0.30:
                has_data = 1
                data_in = rng.randint(0, 15)
            elif r < 0.45:
                has_data = 0
                data_in = rng.randint(0, 15)
            else:
                has_data = 0
                data_in = 0
        rows.append({
            'rst': rst & 0x1,
            'data_in': data_in & 0xF,
            'has_data_to_send': has_data & 0x1,
        })
    return rows

def stimulus(rng, cycles):
    rows = []
    rst = 0
    data = 0
    enable = 0
    fault = 0
    clear = 0
    for i in range(cycles):
        if i < 2:
            rst = 0
        elif i == 2:
            rst = 1
        elif i < 40:
            rst = 1
        else:
            rst = 1 if rng.random() > 0.005 else 0
        if rst == 0:
            data = 0
            enable = 0
            fault = 0
            clear = 0
        else:
            r = rng.random()
            if r < 0.30:
                enable = 1
                data = rng.randrange(0, 65536)
                fault = 0
                clear = 0
            elif r < 0.36:
                fault = 1
                enable = 1 if rng.random() < 0.5 else 0
                clear = 0
                data = rng.randrange(0, 65536)
            elif r < 0.42:
                clear = 1
                fault = 1 if rng.random() < 0.4 else 0
                enable = 0
                data = rng.randrange(0, 65536)
            elif r < 0.48:
                enable = 0
                fault = 0
                clear = 0
                data = rng.randrange(0, 65536)
            else:
                enable = 1 if rng.random() < 0.80 else 0
                fault = 0
                clear = 0
                if rng.random() < 0.5:
                    data = rng.randrange(0, 65536)
        row = {
            'i_rst_b': rst,
            'i_data_in': data & 0xFFFF,
            'i_enable': enable,
            'i_fault': fault,
            'i_clear': clear,
        }
        if rst == 1 and rng.random() < 0.18:
            row['mid'] = {
                'i_enable': 1 if rng.random() < 0.5 else 0,
                'i_fault': 1 if rng.random() < 0.3 else 0,
                'i_clear': 1 if rng.random() < 0.2 else 0,
            }
        rows.append(row)
    return rows

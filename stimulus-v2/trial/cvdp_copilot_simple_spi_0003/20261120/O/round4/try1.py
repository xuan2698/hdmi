def stimulus(rng, cycles):
    rows = []
    rst = 0
    data = 0
    enable = 0
    fault = 0
    clear = 0
    for i in range(cycles):
        if i < 3:
            rst = 0
        elif i < 5:
            rst = 1
        else:
            rst = 1 if rng.random() > 0.01 else 0
        if rst == 0:
            data = 0
            enable = 0
            fault = 0
            clear = 0
        else:
            r = rng.random()
            if r < 0.15:
                enable = 1
                data = rng.randrange(0, 65536)
                fault = 0
                clear = 0
            elif r < 0.20:
                fault = 1
                enable = 1
                data = rng.randrange(0, 65536)
                clear = 0
            elif r < 0.25:
                clear = 1
                fault = 0
                enable = 1
                data = rng.randrange(0, 65536)
            elif r < 0.30:
                enable = 0
                fault = 0
                clear = 0
            else:
                enable = 1
                fault = 0
                clear = 0
                if rng.random() < 0.3:
                    data = rng.randrange(0, 65536)
        row = {
            'i_rst_b': rst,
            'i_data_in': data & 0xFFFF,
            'i_enable': enable,
            'i_fault': fault,
            'i_clear': clear,
        }
        rows.append(row)
    return rows

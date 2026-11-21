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
        elif i < 4:
            rst = 1
        else:
            rst = 1 if rng.random() > 0.02 else 0
        if rst == 0:
            data = 0
            enable = 0
            fault = 0
            clear = 0
        else:
            r = rng.random()
            if r < 0.20:
                enable = 1
                data = rng.randrange(0, 65536)
                fault = 0
                clear = 0
            elif r < 0.26:
                fault = 1
                enable = 1
                data = rng.randrange(0, 65536)
                clear = 0
            elif r < 0.32:
                clear = 1
                fault = 0
                enable = 1
                data = rng.randrange(0, 65536)
            elif r < 0.38:
                enable = 0
                fault = 0
                clear = 0
            else:
                enable = 1
                fault = 0
                clear = 0
                if rng.random() < 0.25:
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

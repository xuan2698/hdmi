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
        elif i < 6:
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
            if r < 0.10:
                enable = 1
                data = rng.randrange(0, 65536)
                fault = 0
                clear = 0
            elif r < 0.14:
                fault = 1
                enable = 0
                clear = 0
            elif r < 0.18:
                clear = 1
                fault = 0
                enable = 0
            elif r < 0.22:
                enable = 0
                fault = 0
                clear = 0
            else:
                enable = 1 if rng.random() < 0.80 else 0
                fault = 0
                clear = 0
                if rng.random() < 0.20:
                    data = rng.randrange(0, 65536)
        row = {
            'i_rst_b': rst & 0x1,
            'i_data_in': data & 0xFFFF,
            'i_enable': enable & 0x1,
            'i_fault': fault & 0x1,
            'i_clear': clear & 0x1,
        }
        rows.append(row)
    return rows

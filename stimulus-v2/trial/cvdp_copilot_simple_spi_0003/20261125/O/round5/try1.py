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
        elif i < 6:
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
            if r < 0.15:
                enable = 1
                data = rng.randrange(0, 65536)
                fault = 0
                clear = 0
            elif r < 0.20:
                fault = 1
                enable = 1
                clear = 0
            elif r < 0.25:
                clear = 1
                fault = 0
                enable = 0
            elif r < 0.30:
                enable = 0
                fault = 0
                clear = 0
            else:
                if rng.random() < 0.5:
                    data = rng.randrange(0, 65536)
                enable = 1 if rng.random() < 0.7 else 0
                fault = 0
                clear = 0
        row = {
            'i_rst_b': rst,
            'i_data_in': data & 0xFFFF,
            'i_enable': enable & 1,
            'i_fault': fault & 1,
            'i_clear': clear & 1,
        }
        rows.append(row)
    return rows

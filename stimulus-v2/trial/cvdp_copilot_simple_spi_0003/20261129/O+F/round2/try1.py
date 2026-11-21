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
            data = 0
            enable = 0
            fault = 0
            clear = 0
        elif i < 4:
            rst = 1
            data = 0
            enable = 0
            fault = 0
            clear = 0
        else:
            rst = 1 if rng.random() > 0.01 else 0
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
                elif r < 0.38:
                    fault = 1
                    clear = 0
                    enable = 1 if rng.random() < 0.5 else 0
                    data = rng.randrange(0, 65536)
                elif r < 0.45:
                    clear = 1
                    fault = 0
                    enable = 0
                    data = rng.randrange(0, 65536)
                elif r < 0.50:
                    enable = 0
                    fault = 0
                    clear = 0
                    data = rng.randrange(0, 65536)
                else:
                    enable = 0
                    fault = 0
                    clear = 0
        row = {
            'i_rst_b': rst & 1,
            'i_data_in': data & 0xFFFF,
            'i_enable': enable & 1,
            'i_fault': fault & 1,
            'i_clear': clear & 1,
        }
        rows.append(row)
    return rows

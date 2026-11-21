def stimulus(rng, cycles):
    rows = []
    data = 0
    enable = 0
    fault = 0
    clear = 0
    rst = 0
    for i in range(cycles):
        if i < 2:
            rst = 0
            enable = 0
            fault = 0
            clear = 0
            data = 0
        elif i == 2:
            rst = 1
            enable = 1
            fault = 1
            clear = 1
            data = 0
        else:
            rst = 1
            r = rng.random()
            if i < 6:
                enable = 0
                fault = 0
                clear = 0
            elif r < 0.04:
                fault = 1
                enable = rng.randint(0, 1)
                clear = 0
                data = rng.randint(0, 0xFFFF)
            elif r < 0.08:
                clear = 1
                fault = 0
                enable = rng.randint(0, 1)
                data = rng.randint(0, 0xFFFF)
            elif r < 0.15:
                enable = 0
                fault = 0
                clear = 0
            else:
                enable = 1
                fault = 0
                clear = 0
                if rng.random() < 0.25:
                    data = rng.randint(0, 0xFFFF)
                else:
                    data = (data + rng.randint(1, 4096)) & 0xFFFF
        row = {
            'i_rst_b': rst & 1,
            'i_data_in': data & 0xFFFF,
            'i_enable': enable & 1,
            'i_fault': fault & 1,
            'i_clear': clear & 1,
        }
        rows.append(row)
    return rows

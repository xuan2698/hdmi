def stimulus(rng, cycles):
    rows = []
    data = 0
    enable = 0
    fault = 0
    clear = 0
    rst = 0
    for i in range(cycles):
        if i < 3:
            rst = 0
            enable = 0
            fault = 0
            clear = 0
            data = 0
        elif i < 6:
            rst = 1
            enable = 0
            fault = 0
            clear = 0
            data = 0
        else:
            rst = 1
            r = rng.random()
            if r < 0.05:
                enable = 0
                fault = 0
                clear = 0
            elif r < 0.10:
                enable = 1
                fault = 1
                clear = 0
            elif r < 0.15:
                enable = 1
                fault = 0
                clear = 1
            elif r < 0.20:
                enable = 0
                fault = 0
                clear = 1
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

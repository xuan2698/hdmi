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
        elif i < 6:
            rst = 1
            data = rng.randrange(0, 65536)
            enable = 1
            fault = 0
            clear = 0
        elif i < 8:
            rst = 1
            data = rng.randrange(0, 65536)
            enable = 1
            fault = 1
            clear = 0
        elif i < 10:
            rst = 1
            data = rng.randrange(0, 65536)
            enable = 1
            fault = 0
            clear = 1
        elif i < 12:
            rst = 1
            data = rng.randrange(0, 65536)
            enable = 0
            fault = 0
            clear = 0
        else:
            r = rng.randrange(0, 100)
            if r < 55:
                data = rng.randrange(0, 65536)
                enable = 1
                fault = 0
                clear = 0
            elif r < 68:
                data = rng.randrange(0, 65536)
                enable = 0
                fault = 0
                clear = 0
            elif r < 78:
                data = rng.randrange(0, 65536)
                enable = 1
                fault = 1
                clear = 0
            elif r < 86:
                data = rng.randrange(0, 65536)
                enable = 1
                fault = 0
                clear = 1
            elif r < 93:
                data = rng.randrange(0, 65536)
                enable = 0
                fault = 0
                clear = 1
            else:
                data = rng.randrange(0, 65536)
                enable = 1
                fault = 1
                clear = 1
        row = {
            'i_rst_b': rst & 1,
            'i_data_in': data & 0xFFFF,
            'i_enable': enable & 1,
            'i_fault': fault & 1,
            'i_clear': clear & 1,
        }
        rows.append(row)
    return rows

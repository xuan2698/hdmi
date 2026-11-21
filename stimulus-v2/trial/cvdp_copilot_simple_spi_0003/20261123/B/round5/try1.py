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
        else:
            rst = 1
        if i < 5:
            data = 0
            enable = 0
            fault = 0
            clear = 0
        elif i < 10:
            data = rng.randrange(0, 65536)
            enable = 1
            fault = 0
            clear = 0
        elif i < 15:
            data = rng.randrange(0, 65536)
            enable = 0
            fault = 0
            clear = 0
        elif i < 20:
            data = rng.randrange(0, 65536)
            enable = 1
            fault = 1
            clear = 0
        elif i < 25:
            data = rng.randrange(0, 65536)
            enable = 1
            fault = 0
            clear = 1
        else:
            r = rng.randrange(0, 100)
            if r < 70:
                data = rng.randrange(0, 65536)
                enable = 1
                fault = 0
                clear = 0
            elif r < 80:
                data = rng.randrange(0, 65536)
                enable = 0
                fault = 0
                clear = 0
            elif r < 88:
                data = rng.randrange(0, 65536)
                enable = 1
                fault = 1
                clear = 0
            elif r < 94:
                data = rng.randrange(0, 65536)
                enable = 1
                fault = 0
                clear = 1
            else:
                data = rng.randrange(0, 65536)
                enable = 0
                fault = 0
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

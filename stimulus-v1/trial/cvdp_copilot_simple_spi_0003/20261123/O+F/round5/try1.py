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
        elif i < 4:
            rst = 1
            enable = 0
            fault = 0
            clear = 0
            data = 0
        elif i < 60:
            rst = 1
            enable = 1
            fault = 0
            clear = 0
            if i == 4:
                data = 0xFFFF
            elif i == 5:
                data = 0x0000
            elif i == 6:
                data = 0xAAAA
            elif i == 7:
                data = 0x5555
            elif rng.random() < 0.25:
                data = rng.randrange(0, 65536)
        elif i < 70:
            rst = 1
            enable = 1
            fault = 1
            clear = 0
            if rng.random() < 0.3:
                data = rng.randrange(0, 65536)
        elif i < 80:
            rst = 1
            enable = 1
            fault = 0
            clear = 1
        elif i < 90:
            rst = 1
            enable = 0
            fault = 0
            clear = 0
        else:
            rst = 1
            r = rng.random()
            if r < 0.04:
                enable = 0
                fault = 0
                clear = 0
            elif r < 0.08:
                enable = 1
                fault = 1
                clear = 0
            elif r < 0.12:
                enable = 1
                fault = 0
                clear = 1
            elif r < 0.16:
                enable = 0
                fault = 0
                clear = 1
            elif r < 0.20:
                enable = 0
                fault = 1
                clear = 0
            else:
                enable = 1
                fault = 0
                clear = 0
            if rng.random() < 0.35:
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

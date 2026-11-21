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
            phase = (i - 6) % 200
            if phase < 40:
                enable = 1
                fault = 0
                clear = 0
                if phase == 0:
                    data = rng.randrange(0, 65536)
            elif phase < 60:
                enable = 1
                fault = 0
                clear = 0
                if phase == 40:
                    data = rng.randrange(0, 65536)
            elif phase < 70:
                enable = 1
                fault = 1
                clear = 0
            elif phase < 80:
                enable = 1
                fault = 1
                clear = 1
            elif phase < 90:
                enable = 1
                fault = 0
                clear = 1
            elif phase < 100:
                enable = 0
                fault = 0
                clear = 0
            elif phase < 110:
                enable = 0
                fault = 1
                clear = 0
            elif phase < 120:
                enable = 1
                fault = 0
                clear = 0
                if phase == 110:
                    data = rng.randrange(0, 65536)
            elif phase < 130:
                enable = 0
                fault = 0
                clear = 1
            elif phase < 140:
                enable = 1
                fault = 1
                clear = 0
            elif phase < 150:
                enable = 1
                fault = 0
                clear = 0
                if phase == 140:
                    data = rng.randrange(0, 65536)
            elif phase < 160:
                enable = 1
                fault = 0
                clear = 1
            elif phase < 170:
                enable = 0
                fault = 0
                clear = 0
            elif phase < 180:
                enable = 1
                fault = 0
                clear = 0
                if phase == 170:
                    data = rng.randrange(0, 65536)
            else:
                enable = 1
                fault = 0
                clear = 0
                if phase == 180:
                    data = rng.randrange(0, 65536)
            if rng.random() < 0.02:
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

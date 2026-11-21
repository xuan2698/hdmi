def stimulus(rng, cycles):
    rows = []
    data = 0
    enable = 0
    fault = 0
    clear = 0
    rst = 0
    for i in range(cycles):
        if i < 4:
            rst = 0
            enable = 0
            fault = 0
            clear = 0
            data = 0
        elif i < 8:
            rst = 1
            enable = 0
            fault = 0
            clear = 0
            data = 0
        else:
            rst = 1
            r = rng.randrange(100)
            if r < 10:
                enable = 1
                fault = 0
                clear = 0
                data = rng.randrange(1 << 16)
            elif r < 14:
                enable = 1
                fault = 1
                clear = 0
            elif r < 18:
                enable = 1
                fault = 0
                clear = 1
            elif r < 22:
                enable = 0
                fault = 0
                clear = 0
            elif r < 26:
                enable = 0
                fault = 1
                clear = 0
            elif r < 30:
                enable = 0
                fault = 0
                clear = 1
            else:
                if rng.randrange(5) == 0:
                    data = rng.randrange(1 << 16)
        row = {
            'i_rst_b': rst,
            'i_data_in': data & 0xFFFF,
            'i_enable': enable,
            'i_fault': fault,
            'i_clear': clear,
        }
        mid = {}
        if rst == 1 and i >= 8:
            if rng.randrange(11) == 0:
                mid['i_clear'] = 1
            if rng.randrange(17) == 0:
                mid['i_fault'] = 1
            if rng.randrange(13) == 0:
                mid['i_enable'] = 1 - enable
            if rng.randrange(19) == 0:
                mid['i_data_in'] = rng.randrange(1 << 16)
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows

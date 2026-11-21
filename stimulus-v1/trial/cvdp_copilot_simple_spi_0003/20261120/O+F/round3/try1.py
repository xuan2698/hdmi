def stimulus(rng, cycles):
    rows = []
    data = 0
    enable = 0
    fault = 0
    clear = 0
    rst = 0
    for i in range(cycles):
        if i < 2:
            rst = 0; enable = 0; fault = 0; clear = 0; data = 0
        elif i < 6:
            rst = 1; enable = 0; fault = 0; clear = 0; data = 0
        elif i < 50:
            rst = 1; enable = 1; fault = 0; clear = 0
            if i == 6:
                data = 0xA5C3
            elif i == 30:
                data = 0x5A3C
        elif i < 70:
            rst = 1; enable = 1; fault = 0; clear = 0
            if i == 50:
                data = 0xFFFF
        elif i < 90:
            rst = 1; enable = 1; fault = 1; clear = 0
        elif i < 100:
            rst = 1; enable = 1; fault = 0; clear = 1
        elif i < 130:
            rst = 1; enable = 0; fault = 0; clear = 0
        else:
            rst = 1
            r = rng.randrange(100)
            if r < 30:
                enable = 1; fault = 0; clear = 0
                if rng.randrange(3) == 0:
                    data = rng.randrange(1 << 16)
            elif r < 38:
                enable = 1; fault = 1; clear = 0
            elif r < 46:
                enable = 1; fault = 0; clear = 1
            elif r < 60:
                enable = 0; fault = 0; clear = 0
            elif r < 68:
                enable = 0; fault = 1; clear = 0
            elif r < 76:
                enable = 0; fault = 0; clear = 1
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
        if rst == 1 and i >= 6:
            if rng.randrange(20) == 0:
                mid['i_clear'] = 1
            if rng.randrange(25) == 0:
                mid['i_fault'] = 1
            if rng.randrange(18) == 0:
                mid['i_enable'] = 1 - enable
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows

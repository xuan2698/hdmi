def stimulus(rng, cycles):
    rows = []
    rst = 0
    enable = 0
    fault = 0
    clear = 0
    data = 0
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
        elif i < 6:
            rst = 1
            enable = 1
            fault = 0
            clear = 0
            data = rng.randrange(0, 1 << 16)
        else:
            rst = 1
            if rng.random() < 0.04:
                enable = 1 - enable
            if rng.random() < 0.03:
                fault = 1 - fault
            if rng.random() < 0.05:
                clear = 1
            else:
                clear = 0
            if rng.random() < 0.25:
                data = rng.randrange(0, 1 << 16)
        row = {
            'i_rst_b': rst,
            'i_data_in': data,
            'i_enable': enable,
            'i_fault': fault,
            'i_clear': clear,
        }
        if rng.random() < 0.12:
            mid = {}
            if rng.random() < 0.5:
                mid['i_enable'] = 1 - enable
            if rng.random() < 0.3:
                mid['i_fault'] = 1 - fault
            if rng.random() < 0.3:
                mid['i_clear'] = 1 - clear
            if rng.random() < 0.4:
                mid['i_data_in'] = rng.randrange(0, 1 << 16)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows

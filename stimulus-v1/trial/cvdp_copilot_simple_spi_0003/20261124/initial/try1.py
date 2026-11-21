def stimulus(rng, cycles):
    rows = []
    rst = 0
    data = 0
    en = 0
    flt = 0
    clr = 0
    for i in range(cycles):
        if i < 4:
            rst = 0
            data = 0
            en = 0
            flt = 0
            clr = 0
        elif i < 8:
            rst = 1
            data = 0
            en = 0
            flt = 0
            clr = 0
        else:
            rst = 1
            r = rng.random()
            if r < 0.05:
                en = 1
                data = rng.randrange(0, 65536)
                flt = 0
                clr = 0
            elif r < 0.10:
                en = 0
                data = rng.randrange(0, 65536)
                flt = 0
                clr = 0
            elif r < 0.13:
                en = 1
                data = rng.randrange(0, 65536)
                flt = 1
                clr = 0
            elif r < 0.16:
                en = 1
                data = rng.randrange(0, 65536)
                flt = 0
                clr = 1
            elif r < 0.20:
                en = 0
                data = rng.randrange(0, 65536)
                flt = 1
                clr = 0
            elif r < 0.24:
                en = 0
                data = rng.randrange(0, 65536)
                flt = 0
                clr = 1
            elif r < 0.28:
                en = 1
                data = rng.randrange(0, 65536)
                flt = 1
                clr = 1
            else:
                en = 0
                data = rng.randrange(0, 65536)
                flt = 0
                clr = 0
        row = {
            'i_rst_b': rst,
            'i_data_in': data & 0xFFFF,
            'i_enable': en,
            'i_fault': flt,
            'i_clear': clr,
        }
        mid = {}
        if rng.random() < 0.15:
            mid['i_enable'] = rng.randrange(0, 2)
        if rng.random() < 0.10:
            mid['i_fault'] = rng.randrange(0, 2)
        if rng.random() < 0.10:
            mid['i_clear'] = rng.randrange(0, 2)
        if rng.random() < 0.08:
            mid['i_data_in'] = rng.randrange(0, 65536)
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows

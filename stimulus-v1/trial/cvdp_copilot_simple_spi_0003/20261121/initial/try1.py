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
            r = rng.randrange(100)
            if r < 5:
                en = 0
                flt = 0
                clr = 0
            elif r < 10:
                en = 1
                flt = 1
                clr = 0
            elif r < 15:
                en = 1
                flt = 0
                clr = 1
            elif r < 20:
                en = 0
                flt = 1
                clr = 1
            else:
                en = 1
                flt = 0
                clr = 0
            if rng.randrange(4) == 0:
                data = rng.randrange(1 << 16)
            else:
                data = (data + rng.randrange(1, 300)) & 0xFFFF
        row = {
            'i_rst_b': rst,
            'i_data_in': data & 0xFFFF,
            'i_enable': en,
            'i_fault': flt,
            'i_clear': clr,
        }
        if rng.randrange(3) == 0:
            mid = {}
            if rng.randrange(2) == 0:
                mid['i_enable'] = rng.randrange(2)
            if rng.randrange(2) == 0:
                mid['i_fault'] = rng.randrange(2)
            if rng.randrange(2) == 0:
                mid['i_clear'] = rng.randrange(2)
            if rng.randrange(3) == 0:
                mid['i_data_in'] = rng.randrange(1 << 16)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows

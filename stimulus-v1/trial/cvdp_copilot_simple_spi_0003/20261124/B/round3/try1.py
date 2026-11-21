def stimulus(rng, cycles):
    rows = []
    rst = 0
    data = 0
    en = 0
    flt = 0
    clr = 0
    for i in range(cycles):
        if i < 3:
            rst = 0
            data = 0
            en = 0
            flt = 0
            clr = 0
        elif i < 6:
            rst = 1
            data = 0
            en = 0
            flt = 0
            clr = 0
        elif i < 40:
            rst = 1
            en = 1
            flt = 0
            clr = 0
            data = rng.randrange(0, 65536)
        elif i < 80:
            rst = 1
            en = 1
            flt = 0
            clr = 0
            data = (i * 0x9E37) & 0xFFFF
        elif i < 90:
            rst = 1
            en = 1
            flt = 1
            clr = 0
            data = rng.randrange(0, 65536)
        elif i < 100:
            rst = 1
            en = 1
            flt = 0
            clr = 1
            data = rng.randrange(0, 65536)
        elif i < 110:
            rst = 1
            en = 0
            flt = 0
            clr = 0
            data = rng.randrange(0, 65536)
        elif i < 120:
            rst = 1
            en = 1
            flt = 1
            clr = 1
            data = rng.randrange(0, 65536)
        else:
            rst = 1
            r = rng.random()
            if r < 0.28:
                en = 1
                data = rng.randrange(0, 65536)
                flt = 0
                clr = 0
            elif r < 0.42:
                en = 0
                data = rng.randrange(0, 65536)
                flt = 0
                clr = 0
            elif r < 0.54:
                en = 1
                data = rng.randrange(0, 65536)
                flt = 1
                clr = 0
            elif r < 0.64:
                en = 1
                data = rng.randrange(0, 65536)
                flt = 0
                clr = 1
            elif r < 0.74:
                en = 0
                data = rng.randrange(0, 65536)
                flt = 1
                clr = 0
            elif r < 0.84:
                en = 0
                data = rng.randrange(0, 65536)
                flt = 0
                clr = 1
            elif r < 0.92:
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
            'i_rst_b': rst & 1,
            'i_data_in': data & 0xFFFF,
            'i_enable': en & 1,
            'i_fault': flt & 1,
            'i_clear': clr & 1,
        }
        mid = {}
        if rng.random() < 0.10:
            mid['i_enable'] = rng.randrange(0, 2)
        if rng.random() < 0.07:
            mid['i_fault'] = rng.randrange(0, 2)
        if rng.random() < 0.07:
            mid['i_clear'] = rng.randrange(0, 2)
        if rng.random() < 0.05:
            mid['i_data_in'] = rng.randrange(0, 65536)
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows

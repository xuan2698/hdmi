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
        elif i < 60:
            rst = 1
            en = 1
            flt = 0
            clr = 0
            data = (i * 2654435761) & 0xFFFF
        elif i < 90:
            rst = 1
            en = 1
            flt = 0
            clr = 0
            data = rng.randrange(0, 65536)
        elif i < 110:
            rst = 1
            en = 1
            flt = 1
            clr = 0
            data = rng.randrange(0, 65536)
        elif i < 130:
            rst = 1
            en = 1
            flt = 0
            clr = 1
            data = rng.randrange(0, 65536)
        elif i < 150:
            rst = 1
            en = 0
            flt = 0
            clr = 0
            data = rng.randrange(0, 65536)
        elif i < 170:
            rst = 1
            en = 1
            flt = 0
            clr = 0
            data = 0xFFFF
        elif i < 190:
            rst = 1
            en = 1
            flt = 0
            clr = 0
            data = 0x0000
        elif i < 210:
            rst = 1
            en = 1
            flt = 0
            clr = 0
            data = 0xAAAA
        else:
            rst = 1
            r = rng.random()
            if r < 0.30:
                en = 1
                flt = 0
                clr = 0
                data = rng.randrange(0, 65536)
            elif r < 0.45:
                en = 0
                flt = 0
                clr = 0
                data = rng.randrange(0, 65536)
            elif r < 0.55:
                en = 1
                flt = 1
                clr = 0
                data = rng.randrange(0, 65536)
            elif r < 0.65:
                en = 1
                flt = 0
                clr = 1
                data = rng.randrange(0, 65536)
            elif r < 0.75:
                en = 0
                flt = 1
                clr = 0
                data = rng.randrange(0, 65536)
            elif r < 0.85:
                en = 0
                flt = 0
                clr = 1
                data = rng.randrange(0, 65536)
            elif r < 0.92:
                en = 1
                flt = 1
                clr = 1
                data = rng.randrange(0, 65536)
            else:
                en = 0
                flt = 0
                clr = 0
                data = rng.randrange(0, 65536)
        row = {
            'i_rst_b': rst,
            'i_data_in': data & 0xFFFF,
            'i_enable': en,
            'i_fault': flt,
            'i_clear': clr,
        }
        mid = {}
        if rng.random() < 0.12:
            mid['i_enable'] = rng.randrange(0, 2)
        if rng.random() < 0.08:
            mid['i_fault'] = rng.randrange(0, 2)
        if rng.random() < 0.08:
            mid['i_clear'] = rng.randrange(0, 2)
        if rng.random() < 0.06:
            mid['i_data_in'] = rng.randrange(0, 65536)
        if mid:
            row['mid'] = mid
        rows.append(row)
    return rows

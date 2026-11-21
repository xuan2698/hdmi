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
        else:
            rst = 1
            phase = (i - 6) % 200
            if phase < 40:
                en = 1
                flt = 0
                clr = 0
                if phase == 0:
                    data = rng.randrange(0, 65536)
            elif phase < 60:
                en = 0
                flt = 0
                clr = 0
            elif phase < 80:
                en = 1
                flt = 1
                clr = 0
                if phase == 60:
                    data = rng.randrange(0, 65536)
            elif phase < 100:
                en = 1
                flt = 0
                clr = 1
            elif phase < 120:
                en = 0
                flt = 1
                clr = 0
            elif phase < 140:
                en = 0
                flt = 0
                clr = 1
            elif phase < 160:
                en = 1
                flt = 1
                clr = 1
            elif phase < 180:
                en = 0
                flt = 0
                clr = 0
            else:
                en = 1
                flt = 0
                clr = 0
                if phase == 180:
                    data = rng.randrange(0, 65536)
            if rng.random() < 0.02:
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

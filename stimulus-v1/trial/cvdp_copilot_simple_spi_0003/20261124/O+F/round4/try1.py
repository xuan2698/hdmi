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
            phase = (i - 8) % 240
            if phase < 50:
                en = 1
                flt = 0
                clr = 0
                if phase == 0:
                    data = rng.randrange(0, 65536)
            elif phase < 70:
                en = 0
                flt = 0
                clr = 0
            elif phase < 95:
                en = 1
                flt = 1
                clr = 0
                if phase == 70:
                    data = rng.randrange(0, 65536)
            elif phase < 115:
                en = 1
                flt = 0
                clr = 1
            elif phase < 135:
                en = 0
                flt = 1
                clr = 0
            elif phase < 155:
                en = 0
                flt = 0
                clr = 1
            elif phase < 175:
                en = 1
                flt = 1
                clr = 1
            elif phase < 195:
                en = 0
                flt = 0
                clr = 0
            elif phase < 220:
                en = 1
                flt = 0
                clr = 0
                if phase == 195:
                    data = rng.randrange(0, 65536)
            else:
                en = 1
                flt = 0
                clr = 0
                if phase == 220:
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

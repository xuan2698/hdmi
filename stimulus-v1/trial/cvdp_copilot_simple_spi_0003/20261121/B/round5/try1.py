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
            phase = (i - 8) % 128
            if phase < 2:
                en = 0
                flt = 0
                clr = 0
            elif phase < 4:
                en = 1
                flt = 0
                clr = 0
                data = rng.randrange(1 << 16)
            elif phase < 80:
                en = 1
                flt = 0
                clr = 0
                if rng.randrange(10) == 0:
                    data = rng.randrange(1 << 16)
                else:
                    data = (data + rng.randrange(1, 200)) & 0xFFFF
            elif phase < 84:
                en = 1
                flt = 1
                clr = 0
            elif phase < 88:
                en = 1
                flt = 1
                clr = 1
            elif phase < 92:
                en = 1
                flt = 0
                clr = 1
            elif phase < 96:
                en = 0
                flt = 0
                clr = 0
            elif phase < 100:
                en = 1
                flt = 0
                clr = 0
                data = rng.randrange(1 << 16)
            elif phase < 104:
                en = 1
                flt = 0
                clr = 0
                data = 0xFFFF
            elif phase < 108:
                en = 1
                flt = 0
                clr = 0
                data = 0x0000
            elif phase < 112:
                en = 1
                flt = 0
                clr = 0
                data = 0xAAAA
            elif phase < 116:
                en = 1
                flt = 0
                clr = 0
                data = 0x5555
            else:
                en = 1
                flt = 0
                clr = 0
                data = (data + rng.randrange(1, 100)) & 0xFFFF
        row = {
            'i_rst_b': rst,
            'i_data_in': data & 0xFFFF,
            'i_enable': en,
            'i_fault': flt,
            'i_clear': clr,
        }
        if i >= 8 and rng.randrange(3) == 0:
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

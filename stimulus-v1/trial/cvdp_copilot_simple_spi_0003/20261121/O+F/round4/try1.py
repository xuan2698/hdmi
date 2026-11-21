def stimulus(rng, cycles):
    rows = []
    rst = 0
    data = 0
    en = 0
    flt = 0
    clr = 0
    for i in range(cycles):
        if i < 2:
            rst = 0; data = 0; en = 0; flt = 0; clr = 0
        elif i < 5:
            rst = 1; data = 0; en = 0; flt = 0; clr = 0
        elif i < 30:
            rst = 1; en = 1; flt = 0; clr = 0
            data = (i * 0x1234 + 0xABCD) & 0xFFFF
        elif i < 45:
            rst = 1; en = 1; flt = 0; clr = 0
            data = 0xFFFF if (i & 1) else 0x0000
        elif i < 60:
            rst = 1; en = 1; flt = 1; clr = 0
            data = rng.randrange(1 << 16)
        elif i < 70:
            rst = 1; en = 1; flt = 0; clr = 1
            data = rng.randrange(1 << 16)
        elif i < 80:
            rst = 1; en = 0; flt = 0; clr = 0
            data = rng.randrange(1 << 16)
        elif i < 90:
            rst = 1; en = 1; flt = 1; clr = 1
            data = rng.randrange(1 << 16)
        elif i < 100:
            rst = 1; en = 1; flt = 0; clr = 0
            data = 0xAAAA
        else:
            rst = 1
            r = rng.randrange(100)
            if r < 3:
                en = 0; flt = 0; clr = 0
            elif r < 6:
                en = 1; flt = 1; clr = 0
            elif r < 9:
                en = 1; flt = 0; clr = 1
            elif r < 12:
                en = 0; flt = 1; clr = 1
            elif r < 15:
                en = 1; flt = 1; clr = 1
            else:
                en = 1; flt = 0; clr = 0
            if rng.randrange(6) == 0:
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
        if i >= 5 and rng.randrange(5) == 0:
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

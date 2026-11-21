def stimulus(rng, cycles):
    rows = []
    rst = 0
    data = 0
    en = 0
    flt = 0
    clr = 0
    for i in range(cycles):
        if i < 2:
            rst = 0
        elif i < 4:
            rst = 1
        else:
            rst = 1 if rng.random() > 0.01 else 0
        if rst == 0:
            data = 0
            en = 0
            flt = 0
            clr = 0
        else:
            r = rng.random()
            if r < 0.20:
                en = 1
                data = rng.randrange(0, 65536)
                flt = 0
                clr = 0
            elif r < 0.24:
                flt = 1
                en = rng.randrange(0, 2)
                clr = 0
                data = rng.randrange(0, 65536)
            elif r < 0.28:
                clr = 1
                flt = 0
                en = rng.randrange(0, 2)
                data = rng.randrange(0, 65536)
            else:
                en = rng.randrange(0, 2)
                flt = 0
                clr = 0
                if rng.random() < 0.25:
                    data = rng.randrange(0, 65536)
        row = {
            'i_rst_b': rst & 1,
            'i_data_in': data & 0xFFFF,
            'i_enable': en & 1,
            'i_fault': flt & 1,
            'i_clear': clr & 1,
        }
        rows.append(row)
    return rows

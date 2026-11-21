def stimulus(rng, cycles):
    rows = []
    rst = 1
    ev = 0
    ed = 0
    dv = 0
    dd = 0
    for c in range(cycles):
        if c < 3:
            rst = 1
        elif c < 6:
            rst = 0
        else:
            rst = 0
        if rst:
            ev = 0
            ed = 0
            dv = 0
            dd = 0
        else:
            if c < 20:
                ev = 1
                ed = rng.randrange(256)
                dv = 1
                dd = rng.randrange(65536)
            elif c < 40:
                ev = 0
                ed = 0
                dv = 0
                dd = 0
            else:
                r = rng.random()
                if r < 0.4:
                    ev = 1
                    ed = rng.randrange(256)
                else:
                    ev = 0
                    ed = 0
                r2 = rng.random()
                if r2 < 0.4:
                    dv = 1
                    dd = rng.randrange(65536)
                else:
                    dv = 0
                    dd = 0
        row = {
            'rst_in': rst,
            'enc_valid_in': ev,
            'enc_data_in': ed,
            'dec_valid_in': dv,
            'dec_data_in': dd,
        }
        rows.append(row)
    return rows

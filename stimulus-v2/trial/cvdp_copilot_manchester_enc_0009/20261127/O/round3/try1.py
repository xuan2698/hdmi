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
            r = rng.random()
            if r < 0.45:
                ev = 1
                ed = rng.randrange(256)
            else:
                ev = 0
                ed = 0
            r2 = rng.random()
            if r2 < 0.45:
                dv = 1
                mode = rng.randrange(4)
                if mode == 0:
                    dd = rng.randrange(65536)
                elif mode == 1:
                    dd = 0
                    for i in range(8):
                        b = rng.randrange(4)
                        if b == 0:
                            dd |= (1 << (2 * i))
                        elif b == 1:
                            dd |= (1 << (2 * i + 1))
                        elif b == 2:
                            dd |= (3 << (2 * i))
                elif mode == 2:
                    dd = 0
                    for i in range(8):
                        if rng.random() < 0.5:
                            dd |= (1 << (2 * i))
                        else:
                            dd |= (1 << (2 * i + 1))
                else:
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

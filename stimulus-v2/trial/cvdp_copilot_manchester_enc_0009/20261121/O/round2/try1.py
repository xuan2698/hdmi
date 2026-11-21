def stimulus(rng, cycles):
    rows = []
    for i in range(cycles):
        rst = 1 if i < 3 else 0
        ev = ed = dv = dd = 0
        if not rst:
            r = rng.random()
            if r < 0.55:
                ev = 1
                ed = rng.randrange(256)
            elif r < 0.75:
                ev = 1
                ed = 0
            if rng.random() < 0.55:
                dv = 1
                dd = rng.randrange(65536)
            elif rng.random() < 0.3:
                dv = 1
                dd = 0
        rows.append({
            'rst_in': rst,
            'enc_valid_in': ev,
            'enc_data_in': ed,
            'dec_valid_in': dv,
            'dec_data_in': dd,
        })
    return rows

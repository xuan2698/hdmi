def reference(vectors):
    eo = ev = do = dv = 0
    res = []
    for i, row in enumerate(vectors):
        rst = row.get('rst_in', 0) & 1
        evi = row.get('enc_valid_in', 0) & 1
        edi = row.get('enc_data_in', 0) & 255
        dvi = row.get('dec_valid_in', 0) & 1
        ddi = row.get('dec_data_in', 0) & 65535
        if rst:
            eo = ev = do = dv = 0
        res.append({
            'enc_valid_out': ev,
            'enc_data_out': eo,
            'dec_valid_out': dv,
            'dec_data_out': do
        })
        if i % 2 == 0 and not rst:
            e = 0
            for b in range(8):
                if (edi >> b) & 1:
                    e |= 1 << (2 * b)
                else:
                    e |= 2 << (2 * b)
            eo = e & 0xFFFF
            ev = evi
            d = 0
            for b in range(8):
                p = (ddi >> (2 * b)) & 3
                if p == 1:
                    d |= 1 << b
            do = d & 0xFF
            dv = dvi
    return res

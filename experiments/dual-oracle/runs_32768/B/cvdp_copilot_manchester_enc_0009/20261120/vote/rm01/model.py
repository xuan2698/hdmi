def reference(vectors):
    enc_v = enc_d = dec_v = dec_d = 0
    out = []
    for i, row in enumerate(vectors):
        pos = (i % 2 == 0)
        if 'clk_in' in row:
            pos = int(row['clk_in']) != 0
        elif 'clk' in row:
            pos = int(row['clk']) != 0
        elif 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                s = e.lower()
                pos = ('pos' in s) or ('rise' in s) or (s == '1')
            else:
                pos = bool(e)
        elif 'posedge' in row:
            pos = bool(row['posedge'])
        elif 'negedge' in row:
            pos = not bool(row['negedge'])

        rst = int(row.get('rst_in', 0)) & 1
        if rst:
            enc_v = 0
            enc_d = 0
            dec_v = 0
            dec_d = 0

        out.append({
            'enc_valid_out': enc_v & 1,
            'enc_data_out': enc_d & 0xFFFF,
            'dec_valid_out': dec_v & 1,
            'dec_data_out': dec_d & 0xFF
        })

        if pos and not rst:
            ev = int(row.get('enc_valid_in', 0)) & 1
            edi = int(row.get('enc_data_in', 0)) & 0xFF
            dv = int(row.get('dec_valid_in', 0)) & 1
            ddi = int(row.get('dec_data_in', 0)) & 0xFFFF

            end = 0
            for b in range(8):
                pair = 1 if ((edi >> b) & 1) else 2
                end |= pair << (2 * b)

            ddn = 0
            for b in range(8):
                pair = (ddi >> (2 * b)) & 3
                if pair == 1:
                    ddn |= 1 << b

            enc_v = ev
            enc_d = end
            dec_v = dv
            dec_d = ddn

    return out

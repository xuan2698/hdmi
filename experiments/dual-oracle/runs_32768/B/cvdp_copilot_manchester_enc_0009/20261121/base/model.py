def reference(vectors):
    ev = 0
    ed = 0
    dv = 0
    dd = 0
    out = []
    for i, row in enumerate(vectors):
        rst = int(row.get('rst_in', 0)) & 1 if isinstance(row, dict) else 0
        if rst:
            ev = ed = dv = dd = 0
        if isinstance(row, dict):
            e = row.get('edge', None)
            if e is None:
                e = row.get('Edge', None)
            if e is not None:
                if isinstance(e, str):
                    s = e.lower()
                    pos = ('pos' in s) or (s in ('1', 'rise', 'rising', 'true'))
                else:
                    pos = bool(e)
            else:
                pos = None
                for k in ('clk_in', 'clk', 'clock'):
                    if k in row:
                        pos = bool(row[k])
                        break
                if pos is None:
                    pos = (i % 2 == 0)
        else:
            pos = (i % 2 == 0)
        out.append({
            'enc_valid_out': ev & 1,
            'enc_data_out': ed & 0xFFFF,
            'dec_valid_out': dv & 1,
            'dec_data_out': dd & 0xFF
        })
        if isinstance(row, dict) and pos and not rst:
            eiv = int(row.get('enc_valid_in', 0)) & 1
            edi = int(row.get('enc_data_in', 0)) & 0xFF
            enc = 0
            for b in range(8):
                if (edi >> b) & 1:
                    enc |= 1 << (2 * b)
                else:
                    enc |= 1 << (2 * b + 1)
            if eiv:
                ed = enc & 0xFFFF
            ev = eiv
            div = int(row.get('dec_valid_in', 0)) & 1
            ddi = int(row.get('dec_data_in', 0)) & 0xFFFF
            dec = 0
            for b in range(8):
                if ((ddi >> (2 * b)) & 3) == 1:
                    dec |= 1 << b
            if div:
                dd = dec & 0xFF
            dv = div
    return out

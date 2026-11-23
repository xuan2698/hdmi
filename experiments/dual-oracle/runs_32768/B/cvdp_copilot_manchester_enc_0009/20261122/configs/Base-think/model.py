def reference(vectors):
    N = 8
    enc_v = enc_d = dec_v = dec_d = 0
    out = []
    for idx, row in enumerate(vectors):
        if isinstance(row, dict):
            rst = row.get('rst_in', 0)
            ev = row.get('enc_valid_in', 0)
            ed = row.get('enc_data_in', 0)
            dv = row.get('dec_valid_in', 0)
            dd = row.get('dec_data_in', 0)
            if 'edge' in row:
                e = row['edge']
                if isinstance(e, str):
                    s = e.lower()
                    pos = ('pos' in s or 'rise' in s or s in ('1', 'p'))
                else:
                    pos = bool(e)
            elif 'clk_in' in row:
                pos = (row['clk_in'] == 1)
            else:
                pos = (idx % 2 == 0)
        else:
            L = len(row)
            if L >= 6:
                e = row[0]
                if isinstance(e, str):
                    s = e.lower()
                    pos = ('pos' in s or 'rise' in s or s in ('1', 'p'))
                else:
                    pos = bool(e)
                rst = row[1]
                ev = row[2]
                ed = row[3]
                dv = row[4]
                dd = row[5]
            else:
                pos = (idx % 2 == 0)
                rst = row[0] if L > 0 else 0
                ev = row[1] if L > 1 else 0
                ed = row[2] if L > 2 else 0
                dv = row[3] if L > 3 else 0
                dd = row[4] if L > 4 else 0
        rst = int(rst) & 1
        ev = int(ev) & 1
        ed = int(ed) & ((1 << N) - 1)
        dv = int(dv) & 1
        dd = int(dd) & ((1 << (2 * N)) - 1)
        if rst:
            enc_v = enc_d = dec_v = dec_d = 0
        out.append({
            'enc_valid_out': enc_v & 1,
            'enc_data_out': enc_d & ((1 << (2 * N)) - 1),
            'dec_valid_out': dec_v & 1,
            'dec_data_out': dec_d & ((1 << N) - 1)
        })
        if pos and not rst:
            e = 0
            for i in range(N):
                bit = (ed >> i) & 1
                pair = 1 if bit else 2
                e |= pair << (2 * i)
            enc_d = e
            enc_v = ev
            d = 0
            for i in range(N):
                pair = (dd >> (2 * i)) & 3
                if pair == 1:
                    d |= 1 << i
            dec_d = d
            dec_v = dv
    return out

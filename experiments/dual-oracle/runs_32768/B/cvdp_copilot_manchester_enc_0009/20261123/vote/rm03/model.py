def reference(vectors):
    N = 8
    eo = 0
    ev = 0
    do = 0
    dv = 0

    if isinstance(vectors, dict):
        vals = list(vectors.values())
        if vals and isinstance(vals[0], (list, tuple)):
            m = len(vals[0])
            rows = []
            for i in range(m):
                d = {}
                for k, v in vectors.items():
                    d[k] = v[i]
                rows.append(d)
            vectors = rows
        else:
            vectors = [vectors]

    res = []
    for idx, row in enumerate(vectors):
        if not isinstance(row, dict):
            row = {}

        rst = int(row.get('rst_in', 0))
        if rst:
            eo = 0
            ev = 0
            do = 0
            dv = 0

        e = None
        if 'edge' in row:
            x = row['edge']
            if isinstance(x, str):
                y = x.lower()
                if y.startswith('pos') or y in ('1', 'p', 'rise', 'rising', 'true'):
                    e = 1
                elif y.startswith('neg') or y in ('0', 'n', 'fall', 'falling', 'false'):
                    e = 0
                else:
                    try:
                        e = 1 if int(x) else 0
                    except:
                        e = None
            else:
                e = 1 if int(x) else 0
        elif 'clk_in' in row:
            e = 1 if int(row['clk_in']) else 0
        elif 'clk' in row:
            e = 1 if int(row['clk']) else 0

        if e is None:
            e = 1 if (idx % 2 == 0) else 0

        res.append({
            'enc_valid_out': ev & 1,
            'enc_data_out': eo & 0xffff,
            'dec_valid_out': dv & 1,
            'dec_data_out': do & 0xff
        })

        if e == 1 and rst == 0:
            enc_v = int(row.get('enc_valid_in', 0)) & 1
            dec_v = int(row.get('dec_valid_in', 0)) & 1
            enc_i = int(row.get('enc_data_in', 0)) & 0xff
            dec_i = int(row.get('dec_data_in', 0)) & 0xffff

            if enc_v:
                ne = 0
                for i in range(N):
                    pair = 1 if ((enc_i >> i) & 1) else 2
                    ne |= pair << (2 * i)
                eo = ne

            if dec_v:
                nd = 0
                for i in range(N):
                    pair = (dec_i >> (2 * i)) & 3
                    if pair == 1:
                        nd |= 1 << i
                do = nd

            ev = enc_v
            dv = dec_v

    return res

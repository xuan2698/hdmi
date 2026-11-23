def reference(vectors):
    N = 8
    enc_valid_reg = 0
    enc_data_reg = 0
    dec_valid_reg = 0
    dec_data_reg = 0
    results = []
    prev_clk = None

    for idx, row in enumerate(vectors):
        if isinstance(row, dict):
            rst = int(row.get('rst_in', 0))
            enc_valid_in = int(row.get('enc_valid_in', 0))
            enc_data_in = int(row.get('enc_data_in', 0))
            dec_valid_in = int(row.get('dec_valid_in', 0))
            dec_data_in = int(row.get('dec_data_in', 0))
            edge = row.get('edge', None)
            clk = row.get('clk_in', None)
        else:
            vals = list(row)
            rst = enc_valid_in = enc_data_in = dec_valid_in = dec_data_in = 0
            edge = None
            clk = None

            last = vals[-1] if vals else None
            last_edge = False
            if isinstance(last, str):
                e = last.lower()
                if ('pos' in e or 'neg' in e or 'rise' in e or 'fall' in e or
                    e in ('0', '1', 'up', 'down') or e.startswith('p') or
                    e.startswith('n') or e.startswith('u') or e.startswith('d')):
                    last_edge = True
            elif isinstance(last, bool):
                last_edge = True

            if len(vals) >= 6 and last_edge:
                if len(vals) >= 7:
                    clk = vals[0]
                    rst, enc_valid_in, enc_data_in, dec_valid_in, dec_data_in = vals[1:6]
                    edge = vals[6]
                else:
                    rst, enc_valid_in, enc_data_in, dec_valid_in, dec_data_in, edge = vals[:6]
            elif len(vals) >= 6:
                clk, rst, enc_valid_in, enc_data_in, dec_valid_in, dec_data_in = vals[:6]
                if len(vals) > 6:
                    edge = vals[6]
            elif len(vals) >= 5:
                rst, enc_valid_in, enc_data_in, dec_valid_in, dec_data_in = vals[:5]
                if len(vals) > 5:
                    edge = vals[5]
            else:
                if len(vals) > 0:
                    rst = vals[0]
                if len(vals) > 1:
                    enc_valid_in = vals[1]
                if len(vals) > 2:
                    enc_data_in = vals[2]
                if len(vals) > 3:
                    dec_valid_in = vals[3]
                if len(vals) > 4:
                    dec_data_in = vals[4]
                if len(vals) > 5:
                    edge = vals[5]

        rst = int(rst) & 1
        enc_valid_in = int(enc_valid_in) & 1
        enc_data_in = int(enc_data_in) & 0xFF
        dec_valid_in = int(dec_valid_in) & 1
        dec_data_in = int(dec_data_in) & 0xFFFF

        is_posedge = False
        if edge is not None:
            if isinstance(edge, str):
                e = edge.lower()
                if 'pos' in e or e in ('1', 'rise', 'rising', 'up') or e.startswith('p') or e.startswith('u'):
                    is_posedge = True
                elif 'neg' in e or e in ('0', 'fall', 'falling', 'down') or e.startswith('n') or e.startswith('d') or e.startswith('f'):
                    is_posedge = False
                else:
                    try:
                        is_posedge = bool(int(edge))
                    except:
                        is_posedge = False
            else:
                is_posedge = bool(edge)
        else:
            if clk is not None:
                c = int(clk)
                if prev_clk is None:
                    is_posedge = (idx % 2 == 0)
                else:
                    is_posedge = (c == 1 and prev_clk == 0)
            else:
                is_posedge = (idx % 2 == 0)

        if clk is not None:
            prev_clk = int(clk)

        if rst:
            enc_valid_reg = 0
            enc_data_reg = 0
            dec_valid_reg = 0
            dec_data_reg = 0
            results.append({
                'enc_valid_out': 0,
                'enc_data_out': 0,
                'dec_valid_out': 0,
                'dec_data_out': 0
            })
            continue

        results.append({
            'enc_valid_out': enc_valid_reg & 1,
            'enc_data_out': enc_data_reg & 0xFFFF,
            'dec_valid_out': dec_valid_reg & 1,
            'dec_data_out': dec_data_reg & 0xFF
        })

        if is_posedge:
            enc_next = 0
            for i in range(N):
                if (enc_data_in >> i) & 1:
                    enc_next |= 1 << (2 * i)
                else:
                    enc_next |= 2 << (2 * i)

            dec_next = 0
            for i in range(N):
                pair = (dec_data_in >> (2 * i)) & 3
                if pair == 1:
                    dec_next |= 1 << i

            enc_valid_reg = enc_valid_in
            enc_data_reg = enc_next & 0xFFFF
            dec_valid_reg = dec_valid_in
            dec_data_reg = dec_next & 0xFF

    return results

def reference(vectors):
    tr = 1
    tok = 0
    dout = 0
    prev_clk = None
    idx = 0
    last_rst = 0
    last_data = 0
    last_has = 0
    res = []

    for v in vectors:
        if isinstance(v, dict):
            if 'rst' in v:
                last_rst = v['rst']
            if 'data_in' in v:
                last_data = v['data_in']
            if 'has_data_to_send' in v:
                last_has = v['has_data_to_send']

            edge = None
            if v.get('posedge', 0):
                edge = 'posedge'
            elif v.get('negedge', 0):
                edge = 'negedge'
            elif 'edge' in v:
                e = v['edge']
                if isinstance(e, str):
                    le = e.lower()
                    if 'pos' in le or e in ('+', '1'):
                        edge = 'posedge'
                    elif 'neg' in le or e in ('-', '0'):
                        edge = 'negedge'
                else:
                    edge = 'posedge' if e else 'negedge'
            elif 'clk' in v:
                clk = v['clk']
                if prev_clk is None:
                    edge = 'posedge' if clk == 1 else 'negedge'
                else:
                    if prev_clk == 0 and clk == 1:
                        edge = 'posedge'
                    elif prev_clk == 1 and clk == 0:
                        edge = 'negedge'
                    else:
                        edge = 'posedge' if (idx % 2 == 0) else 'negedge'
                prev_clk = clk
            else:
                edge = 'posedge' if (idx % 2 == 0) else 'negedge'
        else:
            edge = 'posedge' if (idx % 2 == 0) else 'negedge'

        rst = last_rst
        data_in = last_data & 0xF
        has = last_has

        if rst:
            tr = 1
            tok = 0
            dout = 0
            res.append({'data_out': 0, 'token_received': 1, 'token': 0})
            idx += 1
            continue

        if edge == 'posedge':
            res.append({'data_out': dout, 'token_received': tr, 'token': tok})

            if tr in (1, 2, 4, 8):
                nxt_tr = ((tr << 1) & 0xF)
                if tr & 8:
                    nxt_tr |= 1
                nxt_dout = data_in if has else 0
                nxt_tok = nxt_tr
            else:
                nxt_tr = 1
                nxt_dout = 0
                nxt_tok = 0

            tr = nxt_tr & 0xF
            tok = nxt_tok & 0xF
            dout = nxt_dout & 0xF
        else:
            res.append({'data_out': dout, 'token_received': tr, 'token': tok})

        idx += 1

    return res

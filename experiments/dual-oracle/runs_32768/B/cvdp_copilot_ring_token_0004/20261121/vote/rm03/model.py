def reference(vectors):
    node = 0
    tr = 1
    tok = 0
    dout = 0
    result = []
    for i, row in enumerate(vectors):
        rst = row.get('rst', 0) if isinstance(row, dict) else 0
        data_in = row.get('data_in', 0) if isinstance(row, dict) else 0
        has = row.get('has_data_to_send', 0) if isinstance(row, dict) else 0
        rst = 1 if rst else 0
        has = 1 if has else 0
        data_in = data_in & 0xF

        posedge = None
        if isinstance(row, dict):
            if 'edge' in row:
                ev = row['edge']
                if isinstance(ev, str):
                    posedge = ev.lower().startswith('pos')
                else:
                    posedge = bool(ev)
            elif 'clk' in row:
                posedge = bool(row['clk'])
        if posedge is None:
            posedge = (i % 2 == 0)

        if rst:
            node = 0
            tr = 1
            tok = 0
            dout = 0

        result.append({
            'data_out': dout & 0xF,
            'token_received': tr & 0xF,
            'token': tok & 0xF
        })

        if posedge and not rst:
            next_dout = data_in if has else 0
            next_tok = tr
            next_node = (node + 1) % 4
            next_tr = 1 << next_node
            node = next_node
            tr = next_tr
            tok = next_tok
            dout = next_dout

    return result

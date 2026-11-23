def reference(vectors):
    token_received = 1
    prev_clk = None
    res = []
    for i, row in enumerate(vectors):
        rst = row.get('rst', 0)
        is_posedge = False
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                s = e.lower()
                is_posedge = ('pos' in s) or ('rise' in s) or (s == '1') or (s == 'up')
            else:
                is_posedge = bool(e)
        elif 'clk' in row:
            clk = row['clk']
            if prev_clk is not None:
                is_posedge = (prev_clk == 0 and clk == 1)
            else:
                is_posedge = (clk == 1)
            prev_clk = clk
        else:
            is_posedge = (i % 2 == 0)
        
        if rst == 1:
            token_received = 1
        
        if rst == 1:
            data_out = 0
            token_out = 0
            tr_out = 1
        else:
            tr_out = token_received
            if token_received == 1:
                nxt = 2
            elif token_received == 2:
                nxt = 4
            elif token_received == 4:
                nxt = 8
            elif token_received == 8:
                nxt = 1
            else:
                nxt = 1
            token_out = nxt
            if token_received in (1, 2, 4, 8) and row.get('has_data_to_send', 0) == 1:
                data_out = row.get('data_in', 0) & 0xF
            else:
                data_out = 0
        
        res.append({'data_out': data_out, 'token_received': tr_out, 'token': token_out})
        
        if is_posedge and rst != 1:
            token_received = token_out
    return res

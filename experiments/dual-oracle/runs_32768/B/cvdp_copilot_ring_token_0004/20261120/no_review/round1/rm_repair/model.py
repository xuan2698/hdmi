def reference(vectors):
    state = 1
    token = 0
    data_out = 0
    res = []
    prev_clk = 0
    for i, v in enumerate(vectors):
        if 'edge' in v:
            posedge = (v['edge'] == 'posedge')
        elif 'clk' in v:
            clk = v['clk']
            posedge = (clk == 1 and prev_clk == 0)
            prev_clk = clk
        else:
            posedge = (i % 2 == 0)
        rst = v.get('rst', 0)
        data_in = v.get('data_in', 0) & 0xF
        has = v.get('has_data_to_send', 0)
        if rst == 1:
            state = 1
            token = 0
            data_out = 0
        res.append({
            'data_out': data_out & 0xF,
            'token_received': state & 0xF,
            'token': token & 0xF
        })
        if posedge and rst == 0:
            if state in (1, 2, 4, 8):
                next_state = ((state << 1) | (state >> 3)) & 0xF
                next_token = state
                next_data_out = data_in if has else 0
            else:
                next_state = 1
                next_token = 0
                next_data_out = 0
            state = next_state
            token = next_token
            data_out = next_data_out
    return res

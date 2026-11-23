def reference(vectors):
    state = 0
    res = []
    for i, row in enumerate(vectors):
        r = {str(k).lower(): v for k, v in row.items()} if isinstance(row, dict) else {}
        rst = r.get('rst', 0)
        data_in = r.get('data_in', 0)
        has_data = r.get('has_data_to_send', 0)

        if 'clk' in r:
            is_pos = (r['clk'] == 1)
        elif 'edge' in r:
            e = str(r['edge']).lower()
            is_pos = ('posedge' in e)
        elif 'posedge' in r:
            is_pos = bool(r['posedge'])
        elif 'negedge' in r:
            is_pos = not bool(r['negedge'])
        else:
            is_pos = (i % 2 == 0)

        if rst == 1:
            state = 0
            out_data = 0
            out_tr = 1
            out_t = 0
        else:
            out_tr = 1 << state
            next_state = (state + 1) % 4
            out_t = 1 << next_state
            out_data = data_in if has_data else 0

        res.append({
            'data_out': out_data & 0xF,
            'token_received': out_tr & 0xF,
            'token': out_t & 0xF
        })

        if is_pos and rst == 0:
            state = (state + 1) % 4

    return res

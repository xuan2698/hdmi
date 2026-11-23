def reference(vectors):
    if isinstance(vectors, dict):
        n = len(next(iter(vectors.values())))
        vectors = [{k: vectors[k][i] for k in vectors} for i in range(n)]
    state = 0
    prev_clk = None
    out = []
    for i, row in enumerate(vectors):
        rst = int(row.get('rst', 0))
        data_in = int(row.get('data_in', 0)) & 0xF
        has = int(row.get('has_data_to_send', row.get('has_data', 0)))
        if rst:
            state = 0
        is_pos = (i % 2 == 0)
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                is_pos = e.lower().startswith('pos')
            else:
                is_pos = bool(e)
        elif 'clk' in row:
            clk = int(row['clk'])
            if prev_clk is None:
                is_pos = (clk == 1)
            else:
                is_pos = (prev_clk == 0 and clk == 1)
            prev_clk = clk
        if rst:
            data_out = 0
            token_received = 1
            token = 0
        else:
            token_received = 1 << state
            token = 1 << ((state + 1) & 3)
            data_out = data_in if has else 0
        out.append({
            'data_out': data_out & 0xF,
            'token_received': token_received & 0xF,
            'token': token & 0xF
        })
        if is_pos and not rst:
            state = (state + 1) & 3
    return out

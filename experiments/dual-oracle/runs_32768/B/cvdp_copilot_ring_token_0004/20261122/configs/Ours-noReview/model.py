def reference(vectors):
    state = 0
    out = []
    for idx, row in enumerate(vectors):
        if isinstance(row, dict):
            clk = row.get('clk')
            rst = row.get('rst', 0)
            data_in = row.get('data_in', 0)
            has_data = row.get('has_data_to_send', 0)
        else:
            if len(row) >= 4:
                clk, rst, data_in, has_data = row[0], row[1], row[2], row[3]
            elif len(row) == 3:
                clk = None
                rst, data_in, has_data = row[0], row[1], row[2]
            else:
                clk = None
                rst = data_in = has_data = 0
        try:
            rst = int(rst) & 1
        except:
            rst = 0
        try:
            data_in = int(data_in) & 0xF
        except:
            data_in = 0
        try:
            has_data = int(has_data) & 1
        except:
            has_data = 0
        if clk is None:
            is_posedge = (idx % 2 == 0)
        else:
            if isinstance(clk, str):
                is_posedge = ('pos' in clk.lower())
            else:
                is_posedge = (int(clk) == 1)
        if rst:
            state = 0
        if rst:
            data_out = 0
            token_received = 1
            token = 0
        else:
            token_received = 1 << state
            token = 1 << ((state + 1) % 4)
            data_out = data_in if has_data else 0
        out.append({
            'data_out': data_out,
            'token_received': token_received,
            'token': token
        })
        if is_posedge:
            if rst:
                state = 0
            else:
                state = (state + 1) % 4
    return out

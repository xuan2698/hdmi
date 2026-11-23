def reference(vectors):
    state = 0
    out = []
    for i, row in enumerate(vectors):
        rst = row.get('rst', 0)
        if rst:
            state = 0
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                is_pos = 'pos' in e.lower()
            else:
                is_pos = (e == 1)
        else:
            is_pos = (i % 2 == 0)
        if rst:
            token_received = 1
            token = 0
            data_out = 0
        else:
            token_received = 1 << state
            token = 1 << ((state + 1) % 4)
            if row.get('has_data_to_send', 0):
                data_out = row.get('data_in', 0) & 0xF
            else:
                data_out = 0
        out.append({
            'data_out': data_out,
            'token_received': token_received,
            'token': token
        })
        if is_pos and not rst:
            state = (state + 1) % 4
        elif rst:
            state = 0
    return out

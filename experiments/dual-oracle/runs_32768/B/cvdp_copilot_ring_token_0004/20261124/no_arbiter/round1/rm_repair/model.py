def reference(vectors):
    state = 0
    out = []
    for i, row in enumerate(vectors):
        rst = row.get('rst', 0)
        if rst:
            state = 0

        edge = row.get('edge', None)
        if isinstance(edge, str):
            is_pos = 'pos' in edge.lower()
        elif edge is not None:
            is_pos = (edge == 1)
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

        if rst:
            state = 0
        elif is_pos:
            state = (state + 1) % 4

    return out

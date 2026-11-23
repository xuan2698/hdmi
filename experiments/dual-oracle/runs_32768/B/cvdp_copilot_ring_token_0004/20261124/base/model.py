def reference(vectors):
    state = 1
    out = []
    for i, row in enumerate(vectors):
        rst = row.get('rst', 0) & 1
        data_in = row.get('data_in', 0) & 0xF
        has = row.get('has_data_to_send', 0) & 1

        if rst:
            state = 1

        if rst:
            token_received = 1
            token = 0
            data_out = 0
        else:
            token_received = state
            if state == 1:
                token = 2
            elif state == 2:
                token = 4
            elif state == 4:
                token = 8
            elif state == 8:
                token = 1
            else:
                token = 1
            if has and state in (1, 2, 4, 8):
                data_out = data_in
            else:
                data_out = 0

        out.append({
            'data_out': data_out,
            'token_received': token_received,
            'token': token
        })

        if i % 2 == 0 and not rst:
            state = token

    return out

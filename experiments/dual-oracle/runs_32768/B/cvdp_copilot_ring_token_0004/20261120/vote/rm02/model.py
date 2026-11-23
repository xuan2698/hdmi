def reference(vectors):
    state = 0
    result = []
    for i, row in enumerate(vectors):
        if isinstance(row, dict):
            rst = row.get('rst', 0)
            data_in = row.get('data_in', 0)
            has = row.get('has_data_to_send', 0)
            edge_value = row.get('edge', row.get('clk_edge', None))
            if edge_value is None and 'clk' in row:
                edge_value = row['clk']
            if edge_value is None:
                edge_is_pos = (i % 2 == 0)
            elif isinstance(edge_value, str):
                e = edge_value.lower()
                edge_is_pos = ('pos' in e) or ('rise' in e) or e in ('1', 'p')
            else:
                edge_is_pos = (edge_value == 1)
        else:
            rst = row[0] if len(row) > 0 else 0
            data_in = row[1] if len(row) > 1 else 0
            has = row[2] if len(row) > 2 else 0
            edge_is_pos = (i % 2 == 0)

        rst = 1 if rst else 0
        has = 1 if has else 0
        data_in = int(data_in) & 0xF

        if rst:
            state = 0
            token_received = 1
            token = 0
            data_out = 0
        else:
            token_received = 1 << state
            token = 1 << ((state + 1) & 3)
            data_out = data_in if has else 0

        result.append({
            'data_out': data_out,
            'token_received': token_received,
            'token': token
        })

        if (not rst) and edge_is_pos:
            state = (state + 1) & 3

    return result

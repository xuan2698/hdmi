def reference(vectors):
    node = 0
    prev_clk = None
    result = []

    for i, row in enumerate(vectors):
        if isinstance(row, dict):
            rst = int(row.get('rst', 0))
            data_in = int(row.get('data_in', 0))
            has_data = int(row.get('has_data_to_send', 0))

            posedge = (i % 2 == 0)
            if 'edge' in row:
                edge = str(row['edge']).lower()
                posedge = edge.startswith('pos') or 'rise' in edge or edge == '1'
            elif 'clk' in row:
                clk = int(row['clk'])
                if prev_clk is not None:
                    posedge = (prev_clk == 0 and clk == 1)
                prev_clk = clk
        else:
            rst = 0
            data_in = 0
            has_data = 0
            posedge = (i % 2 == 0)

        if rst:
            node = 0
            token_received = 1
            token = 0
            data_out = 0
        else:
            token_received = 1 << node
            token = 1 << ((node + 1) & 3)
            data_out = (data_in & 0xF) if has_data else 0

        result.append({
            'data_out': data_out & 0xF,
            'token_received': token_received & 0xF,
            'token': token & 0xF
        })

        if posedge and not rst:
            node = (node + 1) & 3

    return result

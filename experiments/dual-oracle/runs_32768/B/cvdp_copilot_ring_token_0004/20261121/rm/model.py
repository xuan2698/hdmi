def reference(vectors):
    state = 1
    results = []
    for i, row in enumerate(vectors):
        # Extract inputs and determine whether this row is a posedge.
        if isinstance(row, dict):
            rst = int(row.get('rst', 0)) & 1
            data_in = int(row.get('data_in', 0)) & 0xF
            has = int(row.get('has_data_to_send', 0)) & 1
            is_pos = (i % 2 == 0)
            if 'edge' in row:
                v = row['edge']
                if isinstance(v, str):
                    s = v.lower()
                    if 'pos' in s or 'rise' in s:
                        is_pos = True
                    elif 'neg' in s or 'fall' in s:
                        is_pos = False
                else:
                    is_pos = bool(v)
            elif 'clk' in row:
                v = row['clk']
                if isinstance(v, str):
                    s = v.lower()
                    if 'pos' in s or 'rise' in s or s == '1':
                        is_pos = True
                    elif 'neg' in s or 'fall' in s or s == '0':
                        is_pos = False
                else:
                    is_pos = bool(v)
            elif 'posedge' in row:
                is_pos = bool(row['posedge'])
            elif 'negedge' in row:
                is_pos = not bool(row['negedge'])
        elif isinstance(row, (list, tuple)):
            vals = list(row)
            is_pos = (i % 2 == 0)
            if vals and isinstance(vals[0], str):
                s = vals[0].lower()
                if 'pos' in s or 'rise' in s:
                    is_pos = True
                    vals = vals[1:]
                elif 'neg' in s or 'fall' in s:
                    is_pos = False
                    vals = vals[1:]
            elif len(vals) == 4 and isinstance(vals[0], (int, bool)) and vals[0] in (0, 1):
                is_pos = bool(vals[0])
                vals = vals[1:]
            if len(vals) >= 3:
                rst = int(vals[0]) & 1
                data_in = int(vals[1]) & 0xF
                has = int(vals[2]) & 1
            elif len(vals) == 2:
                rst = 0
                data_in = int(vals[0]) & 0xF
                has = int(vals[1]) & 1
            elif len(vals) == 1:
                rst = int(vals[0]) & 1
                data_in = 0
                has = 0
            else:
                rst = 0
                data_in = 0
                has = 0
        else:
            rst = 0
            data_in = 0
            has = 0
            is_pos = (i % 2 == 0)

        # Asynchronous active-high reset.
        if rst:
            state = 1

        # Combinational outputs before any registered update.
        if rst:
            data_out = 0
            tr_out = 1
            token_out = 0
        else:
            data_out = data_in if has else 0
            tr_out = state & 0xF
            token_out = ((state << 1) | (state >> 3)) & 0xF

        results.append({
            'data_out': data_out & 0xF,
            'token_received': tr_out & 0xF,
            'token': token_out & 0xF
        })

        # Registered state update on posedge.
        if is_pos:
            if rst:
                state = 1
            else:
                state = token_out

    return results

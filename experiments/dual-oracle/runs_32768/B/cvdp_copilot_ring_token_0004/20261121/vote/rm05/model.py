def reference(vectors):
    node = 0
    out_rows = []
    for i, row in enumerate(vectors):
        if isinstance(row, dict):
            rst = int(row.get('rst', 0))
            data_in = int(row.get('data_in', 0)) & 0xF
            has = int(row.get('has_data_to_send', 0)) & 1
            if 'edge' in row:
                e = row['edge']
                if isinstance(e, str):
                    el = e.lower()
                    if 'pos' in el or el in ('1', 'true', 'high'):
                        is_pos = True
                    elif 'neg' in el or el in ('0', 'false', 'low'):
                        is_pos = False
                    else:
                        is_pos = (i % 2 == 0)
                else:
                    is_pos = bool(e)
            elif 'posedge' in row:
                is_pos = bool(row['posedge'])
            elif 'clk' in row:
                is_pos = (int(row['clk']) == 1)
            else:
                is_pos = (i % 2 == 0)
        else:
            if isinstance(row, (list, tuple)):
                if len(row) >= 3:
                    rst = int(row[0])
                    data_in = int(row[1]) & 0xF
                    has = int(row[2]) & 1
                elif len(row) == 2:
                    rst = int(row[0])
                    data_in = int(row[1]) & 0xF
                    has = 0
                elif len(row) == 1:
                    rst = int(row[0])
                    data_in = 0
                    has = 0
                else:
                    rst = 0
                    data_in = 0
                    has = 0
                if len(row) >= 4:
                    is_pos = (int(row[3]) == 1)
                else:
                    is_pos = (i % 2 == 0)
            else:
                rst = 0
                data_in = 0
                has = 0
                is_pos = (i % 2 == 0)

        if rst:
            node = 0
            out_data = 0
            out_tr = 1
            out_token = 0
        else:
            out_tr = 1 << node
            out_token = 1 << ((node + 1) % 4)
            out_data = data_in if has else 0

        out_rows.append({
            'data_out': out_data,
            'token_received': out_tr,
            'token': out_token
        })

        if is_pos and not rst:
            node = (node + 1) % 4

    return out_rows

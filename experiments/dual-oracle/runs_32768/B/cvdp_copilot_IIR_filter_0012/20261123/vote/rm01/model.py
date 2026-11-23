def reference(vectors):
    q1 = q2 = q3 = 0
    out = []
    for i, row in enumerate(vectors):
        rst = row.get('reset', 0)
        if rst:
            q1 = q2 = q3 = 0
        out.append({
            'out_1': q1 & 0xFFFF,
            'out_2': q2 & 0xFFFF,
            'out_3': q3 & 0xFFFF
        })
        e = row.get('edge', None)
        if e is not None:
            if isinstance(e, str):
                is_pos = e.lower().startswith('pos') or e == '1'
            else:
                is_pos = bool(e)
        elif 'clk' in row:
            is_pos = (row['clk'] == 1)
        else:
            is_pos = (i % 2 == 0)
        if is_pos and not rst:
            q1 = row.get('in_1', 0) & 0xFFFF
            q2 = row.get('in_2', 0) & 0xFFFF
            q3 = row.get('in_3', 0) & 0xFFFF
    return out

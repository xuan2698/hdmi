def reference(vectors):
    c = 0x1F
    out = []
    for i, row in enumerate(vectors):
        e = 'posedge' if i % 2 == 0 else 'negedge'
        r = 0
        if isinstance(row, dict):
            if 'edge' in row:
                e = row['edge']
            if 'reset' in row:
                r = row['reset']
        elif isinstance(row, (list, tuple)):
            if len(row) == 1:
                r = row[0]
            else:
                if isinstance(row[0], str):
                    e, r = row[0], row[1]
                elif isinstance(row[1], str):
                    r, e = row[0], row[1]
                else:
                    r = row[0]
        else:
            r = row

        if isinstance(e, str):
            is_pos = e.lower() in ('posedge', 'pos', '1', 'rising')
        else:
            is_pos = e == 1 or e == '1'

        if r in (1, True, '1'):
            c = 0x1F

        cq = c & 0x1F
        out.append({
            'release_reset_o': 1 if cq < 8 else 0,
            'gate_clk_o': 1 if 0 < cq < 14 else 0,
            'cnt_q': cq
        })

        if is_pos and not (r in (1, True, '1')):
            if c > 0:
                c -= 1
    return out

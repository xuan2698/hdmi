def reference(vectors):
    cnt = 0x1F
    out = []
    for i, row in enumerate(vectors):
        is_pos = (i % 2 == 0)
        reset = 0

        if isinstance(row, dict):
            reset = row.get('reset', 0)
            if 'edge' in row:
                e = row['edge']
                if isinstance(e, str):
                    e_l = e.lower()
                    if e_l.startswith('pos') or e_l == '1':
                        is_pos = True
                    elif e_l.startswith('neg') or e_l == '0':
                        is_pos = False
                else:
                    is_pos = bool(e)
            elif 'clk' in row:
                is_pos = (row['clk'] == 1)
        elif isinstance(row, (list, tuple)):
            if len(row) > 0:
                reset = row[0]
            if len(row) > 1:
                e = row[1]
                if isinstance(e, str):
                    e_l = e.lower()
                    if e_l.startswith('pos') or e_l == '1':
                        is_pos = True
                    elif e_l.startswith('neg') or e_l == '0':
                        is_pos = False
                else:
                    is_pos = (e == 1)
        else:
            reset = row

        if reset:
            cnt = 0x1F

        gate = 1 if 0 < cnt < 0x0E else 0
        release = 1 if cnt < 0x08 else 0

        out.append({
            'cnt_q': cnt & 0x1F,
            'gate_clk_o': gate,
            'release_reset_o': release
        })

        if is_pos and not reset and cnt > 0:
            cnt = (cnt - 1) & 0x1F

    return out

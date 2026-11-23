def reference(vectors):
    state = 0
    ciphertext_reg = 0
    last_reset = 0
    last_start = 0
    last_plaintext = 0
    last_key = 0
    out = []
    for i, row in enumerate(vectors):
        is_posedge = None
        if isinstance(row, dict):
            if 'reset' in row: last_reset = row['reset']
            if 'start' in row: last_start = row['start']
            if 'plaintext' in row: last_plaintext = row['plaintext']
            if 'key' in row: last_key = row['key']
            if 'clk' in row:
                v = row['clk']
                if isinstance(v, str):
                    is_posedge = v.lower() in ('posedge', 'pos', '1', 'rising', 'rise')
                else:
                    is_posedge = (v == 1 or v is True)
            elif 'edge' in row:
                v = row['edge']
                if isinstance(v, str):
                    is_posedge = v.lower() in ('posedge', 'pos', '1', 'rising', 'rise')
                else:
                    is_posedge = (v == 1 or v is True)
            else:
                is_posedge = (i % 2 == 0)
        elif isinstance(row, (list, tuple)):
            if len(row) >= 1 and isinstance(row[0], str):
                v = row[0].lower()
                is_posedge = v in ('posedge', 'pos', '1', 'rising', 'rise')
                if len(row) >= 5:
                    last_reset = row[1]
                    last_start = row[2]
                    last_plaintext = row[3]
                    last_key = row[4]
                elif len(row) >= 4:
                    last_reset = row[1]
                    last_start = row[2]
                    last_plaintext = row[3]
            else:
                if len(row) >= 5:
                    v = row[0]
                    if isinstance(v, str):
                        is_posedge = v.lower() in ('posedge', 'pos', '1', 'rising', 'rise')
                    else:
                        is_posedge = (v == 1 or v is True)
                    last_reset = row[1]
                    last_start = row[2]
                    last_plaintext = row[3]
                    last_key = row[4]
                elif len(row) == 4:
                    is_posedge = (i % 2 == 0)
                    last_reset = row[0]
                    last_start = row[1]
                    last_plaintext = row[2]
                    last_key = row[3]
                else:
                    is_posedge = (i % 2 == 0)
        else:
            is_posedge = (i % 2 == 0)

        if is_posedge is None:
            is_posedge = (i % 2 == 0)

        done = 1 if state == 3 else 0
        out.append({'ciphertext': ciphertext_reg & 0x7fff, 'done': done})

        if is_posedge:
            if last_reset:
                state = 0
                ciphertext_reg = 0
            else:
                if state == 0:
                    if last_start:
                        state = 1
                    else:
                        state = 0
                elif state == 1:
                    state = 2
                elif state == 2:
                    p0 = last_plaintext & 0x1f
                    p1 = (last_plaintext >> 5) & 0x1f
                    p2 = (last_plaintext >> 10) & 0x1f
                    k = last_key
                    k0 = k & 0x1f
                    k1 = (k >> 5) & 0x1f
                    k2 = (k >> 10) & 0x1f
                    k3 = (k >> 15) & 0x1f
                    k4 = (k >> 20) & 0x1f
                    k5 = (k >> 25) & 0x1f
                    k6 = (k >> 30) & 0x1f
                    k7 = (k >> 35) & 0x1f
                    k8 = (k >> 40) & 0x1f
                    s0 = p0 * k0 + p1 * k1 + p2 * k2
                    s1 = p0 * k3 + p1 * k4 + p2 * k5
                    s2 = p0 * k6 + p1 * k7 + p2 * k8
                    o0 = s0 % 26
                    o1 = s1 % 26
                    o2 = s2 % 26
                    ciphertext_reg = (o2 << 10) | (o1 << 5) | o0
                    state = 3
                elif state == 3:
                    state = 0
                else:
                    state = 0
    return out

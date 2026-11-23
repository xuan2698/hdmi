def reference(vectors):
    state = 0
    ciphertext = 0
    s0 = s1 = s2 = 0
    out = []
    prev_clk = 0
    for i, row in enumerate(vectors):
        if 'edge' in row:
            ed = row['edge']
            if isinstance(ed, str):
                posedge = ed.lower() in ('posedge', 'pos', '1')
            else:
                posedge = bool(ed)
        elif 'clk' in row:
            clk = 1 if row['clk'] else 0
            posedge = (prev_clk == 0 and clk == 1)
        else:
            posedge = (i % 2 == 0)
        done = 1 if state == 3 else 0
        out.append({'ciphertext': ciphertext & 0x7fff, 'done': done & 1})
        if posedge:
            if row.get('reset', 0):
                state = 0
                ciphertext = 0
                s0 = s1 = s2 = 0
            else:
                if state == 0:
                    if row.get('start', 0):
                        state = 1
                elif state == 1:
                    p = int(row.get('plaintext', 0)) & 0x7fff
                    k = int(row.get('key', 0)) & ((1 << 45) - 1)
                    p0 = p & 31
                    p1 = (p >> 5) & 31
                    p2 = (p >> 10) & 31
                    k00 = k & 31
                    k01 = (k >> 5) & 31
                    k02 = (k >> 10) & 31
                    k10 = (k >> 15) & 31
                    k11 = (k >> 20) & 31
                    k12 = (k >> 25) & 31
                    k20 = (k >> 30) & 31
                    k21 = (k >> 35) & 31
                    k22 = (k >> 40) & 31
                    s0 = p0 * k00 + p1 * k01 + p2 * k02
                    s1 = p0 * k10 + p1 * k11 + p2 * k12
                    s2 = p0 * k20 + p1 * k21 + p2 * k22
                    state = 2
                elif state == 2:
                    c0 = s0 % 26
                    c1 = s1 % 26
                    c2 = s2 % 26
                    ciphertext = c0 | (c1 << 5) | (c2 << 10)
                    state = 3
                elif state == 3:
                    state = 0
        if 'clk' in row:
            prev_clk = 1 if row['clk'] else 0
    return out

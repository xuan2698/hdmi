def reference(vectors):
    state = 0
    ct = 0
    prev_clk = 0
    res = []
    for idx, row in enumerate(vectors):
        if 'clk' in row:
            clk = row['clk']
            is_posedge = (clk == 1 and prev_clk == 0)
            prev_clk = clk
        elif 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                is_posedge = ('pos' in e.lower() or e == '1')
            else:
                is_posedge = (e == 1)
        else:
            is_posedge = (idx % 2 == 0)
        done = 1 if state == 3 else 0
        res.append({'ciphertext': ct & 0x7FFF, 'done': done})
        if is_posedge:
            reset = row.get('reset', 0)
            if reset:
                state = 0
                ct = 0
            else:
                if state == 0:
                    if row.get('start', 0):
                        state = 1
                elif state == 1:
                    state = 2
                elif state == 2:
                    plaintext = row.get('plaintext', 0)
                    key = row.get('key', 0)
                    p0 = (plaintext >> 10) & 0x1F
                    p1 = (plaintext >> 5) & 0x1F
                    p2 = plaintext & 0x1F
                    k00 = (key >> 40) & 0x1F
                    k01 = (key >> 35) & 0x1F
                    k02 = (key >> 30) & 0x1F
                    k10 = (key >> 25) & 0x1F
                    k11 = (key >> 20) & 0x1F
                    k12 = (key >> 15) & 0x1F
                    k20 = (key >> 10) & 0x1F
                    k21 = (key >> 5) & 0x1F
                    k22 = key & 0x1F
                    c0 = (p0*k00 + p1*k01 + p2*k02) % 26
                    c1 = (p0*k10 + p1*k11 + p2*k12) % 26
                    c2 = (p0*k20 + p1*k21 + p2*k22) % 26
                    ct = (c0 << 10) | (c1 << 5) | c2
                    state = 3
                elif state == 3:
                    state = 0
    return res

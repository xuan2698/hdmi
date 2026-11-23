def reference(vectors):
    state = 0  # 0 IDLE, 1 COMPUTE, 2 COMPUTE_MOD, 3 DONE
    ciphertext = 0
    done = 0
    sums = [0, 0, 0]
    results = []
    prev_clk = 0
    for idx, row in enumerate(vectors):
        results.append({'ciphertext': ciphertext & 0x7fff, 'done': done & 1})
        
        is_pos = None
        if 'clk' in row:
            clk_val = row['clk']
            if clk_val == 1 and prev_clk == 0:
                is_pos = True
            else:
                is_pos = False
            prev_clk = clk_val
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                is_pos = (e.lower() in ('posedge', 'pos', '1'))
            else:
                is_pos = (e == 1)
        if is_pos is None:
            is_pos = (idx % 2 == 0)
        
        if is_pos:
            reset = row.get('reset', 0)
            if reset:
                state = 0
                ciphertext = 0
                done = 0
                sums = [0, 0, 0]
            else:
                if state == 0:  # IDLE
                    if row.get('start', 0):
                        state = 1
                    done = 0
                elif state == 1:  # COMPUTE
                    plaintext = row.get('plaintext', 0)
                    key = row.get('key', 0)
                    p0 = plaintext & 0x1F
                    p1 = (plaintext >> 5) & 0x1F
                    p2 = (plaintext >> 10) & 0x1F
                    for i in range(3):
                        base = i * 3
                        k0 = (key >> (5 * base)) & 0x1F
                        k1 = (key >> (5 * (base + 1))) & 0x1F
                        k2 = (key >> (5 * (base + 2))) & 0x1F
                        sums[i] = p0 * k0 + p1 * k1 + p2 * k2
                    state = 2  # COMPUTE_MOD
                elif state == 2:  # COMPUTE_MOD
                    mod0 = sums[0] % 26
                    mod1 = sums[1] % 26
                    mod2 = sums[2] % 26
                    ciphertext = mod0 | (mod1 << 5) | (mod2 << 10)
                    done = 1
                    state = 3  # DONE
                elif state == 3:  # DONE
                    done = 0
                    state = 0  # IDLE
    return results

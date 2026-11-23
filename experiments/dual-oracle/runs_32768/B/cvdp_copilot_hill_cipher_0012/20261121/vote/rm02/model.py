def reference(vectors):
    state = 0  # 0=IDLE, 1=COMPUTE, 2=COMPUTE_MOD, 3=DONE
    ciphertext = 0
    prev_clk = 0
    results = []
    for i, row in enumerate(vectors):
        reset = row.get('reset', 0)
        start = row.get('start', 0)
        plaintext = row.get('plaintext', 0)
        key = row.get('key', 0)

        if 'clk' in row:
            clk = row['clk']
            posedge = (clk == 1 and prev_clk == 0)
            prev_clk = clk
        else:
            posedge = (i % 2 == 0)

        done = 1 if state == 3 else 0
        results.append({'ciphertext': ciphertext, 'done': done})

        if posedge:
            if reset:
                state = 0
                ciphertext = 0
            else:
                if state == 0:
                    if start:
                        state = 1
                elif state == 1:
                    state = 2
                elif state == 2:
                    p0 = plaintext & 0x1F
                    p1 = (plaintext >> 5) & 0x1F
                    p2 = (plaintext >> 10) & 0x1F

                    k0 = key & 0x1F
                    k1 = (key >> 5) & 0x1F
                    k2 = (key >> 10) & 0x1F
                    k3 = (key >> 15) & 0x1F
                    k4 = (key >> 20) & 0x1F
                    k5 = (key >> 25) & 0x1F
                    k6 = (key >> 30) & 0x1F
                    k7 = (key >> 35) & 0x1F
                    k8 = (key >> 40) & 0x1F

                    c0 = (p0 * k0 + p1 * k1 + p2 * k2) % 26
                    c1 = (p0 * k3 + p1 * k4 + p2 * k5) % 26
                    c2 = (p0 * k6 + p1 * k7 + p2 * k8) % 26

                    ciphertext = c0 | (c1 << 5) | (c2 << 10)
                    state = 3
                elif state == 3:
                    state = 0
    return results

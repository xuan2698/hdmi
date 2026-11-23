def reference(vectors):
    state = 0
    ciphertext = 0
    sum0 = 0
    sum1 = 0
    sum2 = 0
    p_lat = 0
    k_lat = 0
    results = []
    for i, row in enumerate(vectors):
        reset = row.get('reset', 0)
        start = row.get('start', 0)
        plaintext = row.get('plaintext', 0)
        key = row.get('key', 0)
        done = 1 if state == 3 else 0
        results.append({'ciphertext': ciphertext, 'done': done})
        if i % 2 == 0:  # posedge
            if reset:
                state = 0
                ciphertext = 0
                sum0 = sum1 = sum2 = 0
                p_lat = 0
                k_lat = 0
            else:
                if state == 0:
                    if start:
                        p_lat = plaintext
                        k_lat = key
                        state = 1
                elif state == 1:
                    p0 = p_lat & 0x1F
                    p1 = (p_lat >> 5) & 0x1F
                    p2 = (p_lat >> 10) & 0x1F
                    k00 = k_lat & 0x1F
                    k01 = (k_lat >> 5) & 0x1F
                    k02 = (k_lat >> 10) & 0x1F
                    k10 = (k_lat >> 15) & 0x1F
                    k11 = (k_lat >> 20) & 0x1F
                    k12 = (k_lat >> 25) & 0x1F
                    k20 = (k_lat >> 30) & 0x1F
                    k21 = (k_lat >> 35) & 0x1F
                    k22 = (k_lat >> 40) & 0x1F
                    sum0 = p0 * k00 + p1 * k01 + p2 * k02
                    sum1 = p0 * k10 + p1 * k11 + p2 * k12
                    sum2 = p0 * k20 + p1 * k21 + p2 * k22
                    state = 2
                elif state == 2:
                    out0 = sum0 % 26
                    out1 = sum1 % 26
                    out2 = sum2 % 26
                    ciphertext = (out2 << 10) | (out1 << 5) | out0
                    state = 3
                elif state == 3:
                    state = 0
    return results

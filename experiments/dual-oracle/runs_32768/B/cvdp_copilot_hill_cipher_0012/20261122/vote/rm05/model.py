def reference(vectors):
    state = 0
    ciphertext = 0
    done = 0
    sums = [0, 0, 0]
    out = []
    for i, row in enumerate(vectors):
        if 'clk' in row:
            is_pos = int(row.get('clk', 0)) != 0
        else:
            is_pos = (i % 2 == 0)
        out.append({'ciphertext': ciphertext & 0x7fff, 'done': done & 1})
        if not is_pos:
            continue
        if int(row.get('reset', 0)) & 1:
            state = 0
            ciphertext = 0
            done = 0
            sums = [0, 0, 0]
        else:
            start = int(row.get('start', 0)) & 1
            if state == 0:
                done = 0
                if start:
                    state = 1
            elif state == 1:
                pt = int(row.get('plaintext', 0)) & 0x7fff
                key = int(row.get('key', 0)) & ((1 << 45) - 1)
                p0 = pt & 31
                p1 = (pt >> 5) & 31
                p2 = (pt >> 10) & 31
                k0 = key & 31
                k1 = (key >> 5) & 31
                k2 = (key >> 10) & 31
                k3 = (key >> 15) & 31
                k4 = (key >> 20) & 31
                k5 = (key >> 25) & 31
                k6 = (key >> 30) & 31
                k7 = (key >> 35) & 31
                k8 = (key >> 40) & 31
                sums[0] = p0 * k0 + p1 * k1 + p2 * k2
                sums[1] = p0 * k3 + p1 * k4 + p2 * k5
                sums[2] = p0 * k6 + p1 * k7 + p2 * k8
                state = 2
            elif state == 2:
                c0 = sums[0] % 26
                c1 = sums[1] % 26
                c2 = sums[2] % 26
                ciphertext = c0 | (c1 << 5) | (c2 << 10)
                state = 3
            elif state == 3:
                done = 1
                state = 0
    return out

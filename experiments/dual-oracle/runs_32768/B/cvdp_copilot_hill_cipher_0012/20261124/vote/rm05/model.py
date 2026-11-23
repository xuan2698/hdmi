def reference(vectors):
    state = 0  # 0 IDLE, 1 COMPUTE, 2 COMPUTE_MOD, 3 DONE
    cipher = 0
    p_lat = 0
    k_lat = 0
    sum0 = sum1 = sum2 = 0
    out = []
    prev_clk = None
    alt_pos = True

    for row in vectors:
        edge = None
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                s = e.lower()
                if 'pos' in s:
                    edge = 'pos'
                elif 'neg' in s:
                    edge = 'neg'
                else:
                    edge = 'pos' if e.strip() in ('1', 'true') else 'neg'
            else:
                edge = 'pos' if e else 'neg'
        elif 'clk' in row:
            clk = row['clk']
            if prev_clk is None:
                edge = 'pos' if clk else 'neg'
            else:
                if clk == 1 and prev_clk == 0:
                    edge = 'pos'
                elif clk == 0 and prev_clk == 1:
                    edge = 'neg'
                else:
                    edge = 'pos' if clk else 'neg'
            prev_clk = clk
        else:
            edge = 'pos' if alt_pos else 'neg'
            alt_pos = not alt_pos

        reset = row.get('reset', 0)
        start = row.get('start', 0)
        plain = row.get('plaintext', 0)
        key = row.get('key', 0)

        out.append({
            'ciphertext': cipher,
            'done': 1 if state == 3 else 0
        })

        if edge == 'pos':
            if reset:
                state = 0
                cipher = 0
                p_lat = 0
                k_lat = 0
                sum0 = sum1 = sum2 = 0
            else:
                if state == 0:
                    if start:
                        p_lat = plain
                        k_lat = key
                        state = 1
                elif state == 1:
                    p0 = p_lat & 31
                    p1 = (p_lat >> 5) & 31
                    p2 = (p_lat >> 10) & 31

                    k0 = k_lat & 31
                    k1 = (k_lat >> 5) & 31
                    k2 = (k_lat >> 10) & 31
                    k3 = (k_lat >> 15) & 31
                    k4 = (k_lat >> 20) & 31
                    k5 = (k_lat >> 25) & 31
                    k6 = (k_lat >> 30) & 31
                    k7 = (k_lat >> 35) & 31
                    k8 = (k_lat >> 40) & 31

                    sum0 = p0 * k0 + p1 * k1 + p2 * k2
                    sum1 = p0 * k3 + p1 * k4 + p2 * k5
                    sum2 = p0 * k6 + p1 * k7 + p2 * k8
                    state = 2
                elif state == 2:
                    c0 = sum0 % 26
                    c1 = sum1 % 26
                    c2 = sum2 % 26
                    cipher = c0 | (c1 << 5) | (c2 << 10)
                    state = 3
                elif state == 3:
                    state = 0

    return out

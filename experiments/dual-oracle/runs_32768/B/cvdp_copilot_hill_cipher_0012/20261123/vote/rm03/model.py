def reference(vectors):
    IDLE, COMPUTE, COMPUTE_MOD, DONE = 0, 1, 2, 3
    state = IDLE
    ciphertext = 0
    latch_p = 0
    latch_k = 0
    out = []
    prev_clk = 0
    have_prev = False
    for i, row in enumerate(vectors):
        def g(name, default=0):
            if isinstance(row, dict):
                return row.get(name, default)
            return getattr(row, name, default)

        clk = g('clk', None)
        if clk is None:
            posedge = (i % 2 == 0)
        else:
            clk = 1 if clk else 0
            if not have_prev:
                posedge = (clk == 1)
            else:
                posedge = (prev_clk == 0 and clk == 1)

        out.append({
            'ciphertext': ciphertext,
            'done': 1 if state == DONE else 0
        })

        if posedge:
            reset = g('reset', 0)
            if reset:
                state = IDLE
                ciphertext = 0
                latch_p = 0
                latch_k = 0
            else:
                start = g('start', 0)
                plaintext = g('plaintext', 0)
                key = g('key', 0)
                if state == IDLE:
                    if start:
                        latch_p = plaintext & 0x7fff
                        latch_k = key & ((1 << 45) - 1)
                        state = COMPUTE
                elif state == COMPUTE:
                    state = COMPUTE_MOD
                elif state == COMPUTE_MOD:
                    p0 = latch_p & 31
                    p1 = (latch_p >> 5) & 31
                    p2 = (latch_p >> 10) & 31
                    k0 = latch_k & 31
                    k1 = (latch_k >> 5) & 31
                    k2 = (latch_k >> 10) & 31
                    k3 = (latch_k >> 15) & 31
                    k4 = (latch_k >> 20) & 31
                    k5 = (latch_k >> 25) & 31
                    k6 = (latch_k >> 30) & 31
                    k7 = (latch_k >> 35) & 31
                    k8 = (latch_k >> 40) & 31
                    c0 = (p0 * k0 + p1 * k1 + p2 * k2) % 26
                    c1 = (p0 * k3 + p1 * k4 + p2 * k5) % 26
                    c2 = (p0 * k6 + p1 * k7 + p2 * k8) % 26
                    ciphertext = (c0 & 31) | ((c1 & 31) << 5) | ((c2 & 31) << 10)
                    state = DONE
                elif state == DONE:
                    state = IDLE

        if clk is not None:
            prev_clk = clk
            have_prev = True

    return out

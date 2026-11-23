def reference(vectors):
    IDLE = 0
    COMPUTE = 1
    COMPUTE_MOD = 2
    DONE = 3

    state = IDLE
    ciphertext = 0
    sum0 = sum1 = sum2 = 0

    prev_clk = 0
    next_is_pos = True
    results = []

    for row in vectors:
        reset = row.get('reset', 0)
        start = row.get('start', 0)
        plaintext = row.get('plaintext', 0)
        key = row.get('key', 0)

        # Determine whether this row represents a posedge.
        is_pos = None
        if 'clk' in row:
            clk = row['clk']
            if clk == 1 and prev_clk == 0:
                is_pos = True
            elif clk == 0 and prev_clk == 1:
                is_pos = False
            else:
                is_pos = None
            prev_clk = clk
        elif 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                is_pos = e.lower().startswith('pos') or e == '1'
            else:
                is_pos = bool(e)
        else:
            is_pos = next_is_pos
            next_is_pos = not next_is_pos

        # Outputs are read before registered updates at the edge.
        out_done = 1 if state == DONE else 0
        out_ciphertext = ciphertext
        results.append({'ciphertext': out_ciphertext, 'done': out_done})

        # State and register updates occur only on posedge.
        if is_pos:
            if reset:
                state = IDLE
                ciphertext = 0
                sum0 = sum1 = sum2 = 0
            else:
                if state == IDLE:
                    if start:
                        state = COMPUTE
                elif state == COMPUTE:
                    p0 = plaintext & 0x1F
                    p1 = (plaintext >> 5) & 0x1F
                    p2 = (plaintext >> 10) & 0x1F

                    k = [(key >> (5 * i)) & 0x1F for i in range(9)]

                    sum0 = p0 * k[0] + p1 * k[1] + p2 * k[2]
                    sum1 = p0 * k[3] + p1 * k[4] + p2 * k[5]
                    sum2 = p0 * k[6] + p1 * k[7] + p2 * k[8]

                    state = COMPUTE_MOD
                elif state == COMPUTE_MOD:
                    c0 = sum0 % 26
                    c1 = sum1 % 26
                    c2 = sum2 % 26
                    ciphertext = (c2 << 10) | (c1 << 5) | c0
                    state = DONE
                elif state == DONE:
                    state = IDLE

    return results

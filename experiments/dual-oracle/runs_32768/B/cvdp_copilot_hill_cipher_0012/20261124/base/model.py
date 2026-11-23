def reference(vectors):
    IDLE, COMPUTE, COMPUTE_MOD, DONE = 0, 1, 2, 3
    state = IDLE
    ciphertext_reg = 0
    done_reg = 0
    pt_reg = 0
    key_reg = 0
    sum0 = sum1 = sum2 = 0
    last_reset = 0
    last_start = 0
    last_plaintext = 0
    last_key = 0
    prev_clk = None
    edge_toggle = 0
    results = []
    for v in vectors:
        reset = int(v.get('reset', last_reset)) if 'reset' in v else last_reset
        start = int(v.get('start', last_start)) if 'start' in v else last_start
        plaintext = int(v.get('plaintext', last_plaintext)) if 'plaintext' in v else last_plaintext
        key = int(v.get('key', last_key)) if 'key' in v else last_key
        last_reset, last_start, last_plaintext, last_key = reset, start, plaintext, key

        is_posedge = False
        is_negedge = False
        if 'edge' in v:
            e = v['edge']
            if isinstance(e, str):
                el = e.lower()
                if 'pos' in el:
                    is_posedge = True
                elif 'neg' in el:
                    is_negedge = True
            else:
                if e == 1:
                    is_posedge = True
                elif e == 0:
                    is_negedge = True
        if not is_posedge and not is_negedge:
            if 'clk' in v:
                clk_val = int(v['clk'])
                if prev_clk is None:
                    if clk_val == 1:
                        is_posedge = True
                    else:
                        is_negedge = True
                else:
                    if prev_clk == 0 and clk_val == 1:
                        is_posedge = True
                    elif prev_clk == 1 and clk_val == 0:
                        is_negedge = True
                prev_clk = clk_val
            else:
                if edge_toggle % 2 == 0:
                    is_posedge = True
                else:
                    is_negedge = True
                edge_toggle += 1
        else:
            if 'clk' in v:
                prev_clk = int(v['clk'])

        results.append({
            'ciphertext': ciphertext_reg & 0x7FFF,
            'done': done_reg & 1
        })

        if is_posedge:
            if reset:
                state = IDLE
                ciphertext_reg = 0
                done_reg = 0
                pt_reg = 0
                key_reg = 0
                sum0 = sum1 = sum2 = 0
            else:
                if state == IDLE:
                    done_reg = 0
                    if start:
                        pt_reg = plaintext
                        key_reg = key
                        state = COMPUTE
                elif state == COMPUTE:
                    k00 = key_reg & 0x1F
                    k01 = (key_reg >> 5) & 0x1F
                    k02 = (key_reg >> 10) & 0x1F
                    k10 = (key_reg >> 15) & 0x1F
                    k11 = (key_reg >> 20) & 0x1F
                    k12 = (key_reg >> 25) & 0x1F
                    k20 = (key_reg >> 30) & 0x1F
                    k21 = (key_reg >> 35) & 0x1F
                    k22 = (key_reg >> 40) & 0x1F
                    p0 = pt_reg & 0x1F
                    p1 = (pt_reg >> 5) & 0x1F
                    p2 = (pt_reg >> 10) & 0x1F
                    sum0 = k00 * p0 + k01 * p1 + k02 * p2
                    sum1 = k10 * p0 + k11 * p1 + k12 * p2
                    sum2 = k20 * p0 + k21 * p1 + k22 * p2
                    state = COMPUTE_MOD
                elif state == COMPUTE_MOD:
                    ciphertext_reg = (sum0 % 26) | ((sum1 % 26) << 5) | ((sum2 % 26) << 10)
                    done_reg = 1
                    state = DONE
                elif state == DONE:
                    done_reg = 0
                    state = IDLE
    return results

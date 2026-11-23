def reference(vectors):
    IDLE, COMPUTE, COMPUTE_MOD, DONE = 0, 1, 2, 3
    state = IDLE
    ciphertext_reg = 0
    done_reg = 0
    sum0 = sum1 = sum2 = 0
    results = []
    
    for row in vectors:
        reset = row.get('reset', 0)
        start = row.get('start', 0)
        plaintext = row.get('plaintext', 0)
        key = row.get('key', 0)
        edge = row.get('edge', None)
        
        is_pos = False
        if edge is not None:
            if isinstance(edge, str):
                if edge.lower().startswith('pos') or edge == '1':
                    is_pos = True
            else:
                if edge == 1:
                    is_pos = True
        else:
            if row.get('posedge', False):
                is_pos = True
            elif 'clk' in row:
                if row['clk'] == 1:
                    is_pos = True
        
        results.append({
            'ciphertext': ciphertext_reg & 0x7fff,
            'done': done_reg & 1
        })
        
        if is_pos:
            next_state = state
            next_cipher = ciphertext_reg
            next_done = done_reg
            next_sum0, next_sum1, next_sum2 = sum0, sum1, sum2
            
            if reset:
                next_state = IDLE
                next_cipher = 0
                next_done = 0
                next_sum0 = next_sum1 = next_sum2 = 0
            else:
                if state == IDLE:
                    next_done = 0
                    if start:
                        next_state = COMPUTE
                elif state == COMPUTE:
                    p0 = plaintext & 0x1f
                    p1 = (plaintext >> 5) & 0x1f
                    p2 = (plaintext >> 10) & 0x1f

                    k00 = key & 0x1f
                    k01 = (key >> 5) & 0x1f
                    k02 = (key >> 10) & 0x1f
                    k10 = (key >> 15) & 0x1f
                    k11 = (key >> 20) & 0x1f
                    k12 = (key >> 25) & 0x1f
                    k20 = (key >> 30) & 0x1f
                    k21 = (key >> 35) & 0x1f
                    k22 = (key >> 40) & 0x1f

                    next_sum0 = k00 * p0 + k01 * p1 + k02 * p2
                    next_sum1 = k10 * p0 + k11 * p1 + k12 * p2
                    next_sum2 = k20 * p0 + k21 * p1 + k22 * p2
                    next_state = COMPUTE_MOD
                elif state == COMPUTE_MOD:
                    c0 = sum0 % 26
                    c1 = sum1 % 26
                    c2 = sum2 % 26
                    next_cipher = (c2 << 10) | (c1 << 5) | c0
                    next_state = DONE
                elif state == DONE:
                    next_done = 1
                    next_state = IDLE
            
            state = next_state
            ciphertext_reg = next_cipher
            done_reg = next_done
            sum0, sum1, sum2 = next_sum0, next_sum1, next_sum2
    
    return results

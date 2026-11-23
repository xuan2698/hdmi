def reference(vectors):
    state = 0  # 0 IDLE, 1 COMPUTE, 2 COMPUTE_MOD, 3 DONE
    ciphertext = 0
    sum0 = 0
    sum1 = 0
    sum2 = 0
    results = []
    for i, row in enumerate(vectors):
        if isinstance(row, dict):
            reset = row.get('reset', 0)
            start = row.get('start', 0)
            plaintext = row.get('plaintext', 0)
            key = row.get('key', 0)
        else:
            reset = getattr(row, 'reset', 0)
            start = getattr(row, 'start', 0)
            plaintext = getattr(row, 'plaintext', 0)
            key = getattr(row, 'key', 0)
        
        done = 1 if state == 3 else 0
        results.append({'ciphertext': ciphertext & 0x7FFF, 'done': done})
        
        is_posedge = (i % 2 == 0)
        if isinstance(row, dict) and 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                is_posedge = 'pos' in e.lower()
            else:
                is_posedge = bool(e)
        
        if is_posedge:
            if reset:
                state_next = 0
                ciphertext_next = 0
                sum0_next = 0
                sum1_next = 0
                sum2_next = 0
            else:
                state_next = state
                ciphertext_next = ciphertext
                sum0_next = sum0
                sum1_next = sum1
                sum2_next = sum2
                if state == 0:
                    if start:
                        state_next = 1
                elif state == 1:
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
                    sum0_next = p0 * k0 + p1 * k1 + p2 * k2
                    sum1_next = p0 * k3 + p1 * k4 + p2 * k5
                    sum2_next = p0 * k6 + p1 * k7 + p2 * k8
                    state_next = 2
                elif state == 2:
                    c0 = sum0 % 26
                    c1 = sum1 % 26
                    c2 = sum2 % 26
                    ciphertext_next = (c2 << 10) | (c1 << 5) | c0
                    state_next = 3
                elif state == 3:
                    state_next = 0
            state = state_next
            ciphertext = ciphertext_next
            sum0 = sum0_next
            sum1 = sum1_next
            sum2 = sum2_next
    return results

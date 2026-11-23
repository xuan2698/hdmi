def reference(vectors):
    state = 0  # 0: IDLE, 1: COMPUTE, 2: COMPUTE_MOD, 3: DONE
    ciphertext = 0
    pt_latched = 0
    key_latched = 0
    results = []
    for idx, row in enumerate(vectors):
        # Determine if this row is a posedge
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                is_pos = e.lower() in ('posedge', '1', 'p')
            else:
                is_pos = (e == 1)
        elif 'clk' in row:
            is_pos = (row['clk'] == 1)
        else:
            is_pos = (idx % 2 == 0)  # assume first row is posedge

        # Outputs before registered NBA updates
        results.append({
            'ciphertext': ciphertext & 0x7FFF,
            'done': 1 if state == 3 else 0
        })

        # Sequential updates on posedge
        if is_pos:
            reset = row.get('reset', 0)
            start = row.get('start', 0)
            if reset:
                state = 0
                ciphertext = 0
                pt_latched = 0
                key_latched = 0
            else:
                if state == 0:  # IDLE
                    if start:
                        pt_latched = row.get('plaintext', 0) & 0x7FFF
                        key_latched = row.get('key', 0) & ((1 << 45) - 1)
                        state = 1
                elif state == 1:  # COMPUTE
                    state = 2
                elif state == 2:  # COMPUTE_MOD
                    p0 = pt_latched & 0x1F
                    p1 = (pt_latched >> 5) & 0x1F
                    p2 = (pt_latched >> 10) & 0x1F

                    out0 = (
                        ((key_latched & 0x1F) * p0 +
                         ((key_latched >> 5) & 0x1F) * p1 +
                         ((key_latched >> 10) & 0x1F) * p2) % 26
                    ) & 0x1F

                    out1 = (
                        (((key_latched >> 15) & 0x1F) * p0 +
                         ((key_latched >> 20) & 0x1F) * p1 +
                         ((key_latched >> 25) & 0x1F) * p2) % 26
                    ) & 0x1F

                    out2 = (
                        (((key_latched >> 30) & 0x1F) * p0 +
                         ((key_latched >> 35) & 0x1F) * p1 +
                         ((key_latched >> 40) & 0x1F) * p2) % 26
                    ) & 0x1F

                    ciphertext = out0 | (out1 << 5) | (out2 << 10)
                    state = 3
                elif state == 3:  # DONE
                    state = 0

    return results

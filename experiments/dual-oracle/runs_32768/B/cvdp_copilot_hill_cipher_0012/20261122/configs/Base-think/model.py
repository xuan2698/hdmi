def reference(vectors):
    state = 0  # 0=IDLE, 1=COMPUTE, 2=COMPUTE_MOD, 3=DONE
    ciphertext = 0
    latched_plaintext = 0
    latched_key = 0

    cur_reset = 0
    cur_start = 0
    cur_plaintext = 0
    cur_key = 0

    outputs = []

    for row in vectors:
        if 'reset' in row:
            cur_reset = row['reset'] & 1
        if 'start' in row:
            cur_start = row['start'] & 1
        if 'plaintext' in row:
            cur_plaintext = row['plaintext'] & 0x7FFF
        if 'key' in row:
            cur_key = row['key'] & ((1 << 45) - 1)

        done_out = 1 if state == 3 else 0
        ciphertext_out = ciphertext & 0x7FFF
        outputs.append({'ciphertext': ciphertext_out, 'done': done_out})

        edge = row.get('edge', 'posedge')
        if isinstance(edge, str):
            edge = edge.lower()

        if edge == 'posedge' or edge == 'p' or edge == 1:
            if cur_reset:
                state = 0
                ciphertext = 0
            else:
                if state == 0:
                    if cur_start:
                        latched_plaintext = cur_plaintext
                        latched_key = cur_key
                        state = 1
                elif state == 1:
                    state = 2
                elif state == 2:
                    p0 = (latched_plaintext >> 10) & 0x1F
                    p1 = (latched_plaintext >> 5) & 0x1F
                    p2 = latched_plaintext & 0x1F

                    k00 = (latched_key >> 40) & 0x1F
                    k01 = (latched_key >> 35) & 0x1F
                    k02 = (latched_key >> 30) & 0x1F
                    k10 = (latched_key >> 25) & 0x1F
                    k11 = (latched_key >> 20) & 0x1F
                    k12 = (latched_key >> 15) & 0x1F
                    k20 = (latched_key >> 10) & 0x1F
                    k21 = (latched_key >> 5) & 0x1F
                    k22 = latched_key & 0x1F

                    sum0 = p0 * k00 + p1 * k01 + p2 * k02
                    sum1 = p0 * k10 + p1 * k11 + p2 * k12
                    sum2 = p0 * k20 + p1 * k21 + p2 * k22

                    c0 = sum0 % 26
                    c1 = sum1 % 26
                    c2 = sum2 % 26

                    ciphertext = (c0 << 10) | (c1 << 5) | c2
                    state = 3
                elif state == 3:
                    state = 0

    return outputs

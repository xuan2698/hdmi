def reference(vectors):
    state = 0  # 0=IDLE, 1=COMPUTE, 2=COMPUTE_MOD, 3=DONE
    cipher = 0
    sum0 = sum1 = sum2 = 0
    outs = []

    for row in vectors:
        is_pos = True
        if isinstance(row, dict):
            if 'edge' in row:
                e = row['edge']
                if isinstance(e, str):
                    s = e.lower()
                    if 'pos' in s:
                        is_pos = True
                    elif 'neg' in s:
                        is_pos = False
                    else:
                        try:
                            is_pos = int(s) != 0
                        except:
                            is_pos = True
                else:
                    is_pos = bool(e)
            elif 'clk' in row:
                e = row['clk']
                if isinstance(e, str):
                    s = e.lower()
                    is_pos = s not in ('0', 'false', 'neg', 'negedge')
                else:
                    is_pos = bool(e)
            elif 'posedge' in row:
                is_pos = bool(row['posedge'])

        outs.append({
            'ciphertext': cipher & 0x7FFF,
            'done': 1 if state == 3 else 0
        })

        if is_pos:
            reset = 0
            start = 0
            plaintext = 0
            key = 0
            if isinstance(row, dict):
                reset = int(row.get('reset', 0))
                start = int(row.get('start', 0))
                plaintext = int(row.get('plaintext', 0))
                key = int(row.get('key', 0))

            if reset:
                state = 0
                cipher = 0
                sum0 = sum1 = sum2 = 0
            else:
                if state == 0:
                    if start:
                        state = 1
                elif state == 1:
                    p0 = plaintext & 31
                    p1 = (plaintext >> 5) & 31
                    p2 = (plaintext >> 10) & 31

                    k0 = key & 31
                    k1 = (key >> 5) & 31
                    k2 = (key >> 10) & 31
                    k3 = (key >> 15) & 31
                    k4 = (key >> 20) & 31
                    k5 = (key >> 25) & 31
                    k6 = (key >> 30) & 31
                    k7 = (key >> 35) & 31
                    k8 = (key >> 40) & 31

                    sum0 = k0 * p0 + k1 * p1 + k2 * p2
                    sum1 = k3 * p0 + k4 * p1 + k5 * p2
                    sum2 = k6 * p0 + k7 * p1 + k8 * p2
                    state = 2
                elif state == 2:
                    c0 = sum0 % 26
                    c1 = sum1 % 26
                    c2 = sum2 % 26
                    cipher = c0 | (c1 << 5) | (c2 << 10)
                    state = 3
                elif state == 3:
                    state = 0

    return outs

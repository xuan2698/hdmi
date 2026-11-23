def reference(vectors):
    state = 0
    cipher = 0
    sums = [0, 0, 0]
    p_lat = [0, 0, 0]
    k_lat = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    reset = 0
    start = 0
    plaintext = 0
    key = 0
    prev_clk = 0
    out = []

    for row in vectors:
        if 'reset' in row:
            reset = row['reset']
        if 'start' in row:
            start = row['start']
        if 'plaintext' in row:
            plaintext = row['plaintext']
        if 'key' in row:
            key = row['key']

        is_pos = False
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                s = e.lower()
                if s.startswith('p') or s == '1' or s == 'rise' or s == 'rising':
                    is_pos = True
            else:
                if e == 1 or e is True:
                    is_pos = True
        elif 'clk' in row:
            clk = row['clk']
            if clk == 1 and prev_clk == 0:
                is_pos = True
            prev_clk = clk

        out.append({
            'ciphertext': cipher & 0x7fff,
            'done': 1 if state == 3 else 0
        })

        if is_pos:
            if reset:
                state = 0
                cipher = 0
                sums = [0, 0, 0]
                p_lat = [0, 0, 0]
                k_lat = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            else:
                if state == 0:
                    if start:
                        p_lat = [
                            plaintext & 31,
                            (plaintext >> 5) & 31,
                            (plaintext >> 10) & 31
                        ]
                        k_lat = [
                            key & 31,
                            (key >> 5) & 31,
                            (key >> 10) & 31,
                            (key >> 15) & 31,
                            (key >> 20) & 31,
                            (key >> 25) & 31,
                            (key >> 30) & 31,
                            (key >> 35) & 31,
                            (key >> 40) & 31
                        ]
                        state = 1
                elif state == 1:
                    sums = [
                        p_lat[0] * k_lat[0] + p_lat[1] * k_lat[1] + p_lat[2] * k_lat[2],
                        p_lat[0] * k_lat[3] + p_lat[1] * k_lat[4] + p_lat[2] * k_lat[5],
                        p_lat[0] * k_lat[6] + p_lat[1] * k_lat[7] + p_lat[2] * k_lat[8]
                    ]
                    state = 2
                elif state == 2:
                    c0 = sums[0] % 26
                    c1 = sums[1] % 26
                    c2 = sums[2] % 26
                    cipher = c0 | (c1 << 5) | (c2 << 10)
                    state = 3
                elif state == 3:
                    state = 0

    return out

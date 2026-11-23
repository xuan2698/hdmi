def reference(vectors):
    state = 0
    ciphertext = 0
    sums = [0, 0, 0]
    p = [0, 0, 0]
    k = [0] * 9
    prev_clk = 0
    out = []

    for idx, row in enumerate(vectors):
        if isinstance(row, dict):
            def getv(name, default=0):
                if name in row:
                    return row[name]
                up = name.upper()
                if up in row:
                    return row[up]
                return default

            reset = int(getv('reset', 0)) & 1
            start = int(getv('start', 0)) & 1
            plaintext = int(getv('plaintext', 0)) & 0x7FFF
            key = int(getv('key', 0)) & ((1 << 45) - 1)
            edge = getv('edge', None)
            clk = getv('clk', None)

            if edge is not None:
                if isinstance(edge, str):
                    el = edge.lower()
                    posedge = ('pos' in el) or ('rise' in el) or (el in ('1', 'true', 'high'))
                else:
                    posedge = bool(edge)
            elif clk is not None:
                c = int(clk) & 1
                if idx == 0:
                    posedge = (c == 1)
                else:
                    posedge = (prev_clk == 0 and c == 1)
                prev_clk = c
            else:
                posedge = (idx % 2 == 0)
        else:
            vals = list(row)
            posedge = (idx % 2 == 0)

            if vals and isinstance(vals[0], str):
                el = vals[0].lower()
                posedge = ('pos' in el) or ('rise' in el)
                vals = vals[1:]

            if len(vals) >= 5:
                c = int(vals[0]) & 1
                if idx == 0:
                    posedge = (c == 1)
                else:
                    posedge = (prev_clk == 0 and c == 1)
                prev_clk = c
                reset = int(vals[1]) & 1
                start = int(vals[2]) & 1
                plaintext = int(vals[3]) & 0x7FFF
                key = int(vals[4]) & ((1 << 45) - 1)
            elif len(vals) >= 4:
                reset = int(vals[0]) & 1
                start = int(vals[1]) & 1
                plaintext = int(vals[2]) & 0x7FFF
                key = int(vals[3]) & ((1 << 45) - 1)
            else:
                reset = int(vals[0]) & 1 if len(vals) > 0 else 0
                start = int(vals[1]) & 1 if len(vals) > 1 else 0
                plaintext = int(vals[2]) & 0x7FFF if len(vals) > 2 else 0
                key = int(vals[3]) & ((1 << 45) - 1) if len(vals) > 3 else 0

        out.append({
            'ciphertext': ciphertext & 0x7FFF,
            'done': 1 if state == 3 else 0
        })

        if posedge:
            if reset:
                state = 0
                ciphertext = 0
                sums = [0, 0, 0]
                p = [0, 0, 0]
                k = [0] * 9
            else:
                if state == 0:
                    if start:
                        p[0] = plaintext & 0x1F
                        p[1] = (plaintext >> 5) & 0x1F
                        p[2] = (plaintext >> 10) & 0x1F
                        for i in range(9):
                            k[i] = (key >> (5 * i)) & 0x1F
                        state = 1
                elif state == 1:
                    sums[0] = p[0] * k[0] + p[1] * k[1] + p[2] * k[2]
                    sums[1] = p[0] * k[3] + p[1] * k[4] + p[2] * k[5]
                    sums[2] = p[0] * k[6] + p[1] * k[7] + p[2] * k[8]
                    state = 2
                elif state == 2:
                    c0 = sums[0] % 26
                    c1 = sums[1] % 26
                    c2 = sums[2] % 26
                    ciphertext = (c0 & 0x1F) | ((c1 & 0x1F) << 5) | ((c2 & 0x1F) << 10)
                    state = 3
                elif state == 3:
                    state = 0

    return out

def reference(vectors):
    state = 0
    plaintext_reg = 0
    key_reg = 0
    sums = [0, 0, 0]
    ciphertext_reg = 0
    prev_clk = None
    results = []
    for row in vectors:
        is_pos = False
        if isinstance(row, dict):
            if 'edge' in row:
                e = row['edge']
                if isinstance(e, str):
                    el = e.lower()
                    if el in ('posedge', 'pos', 'positive', '1', 'true'):
                        is_pos = True
                    elif el in ('negedge', 'neg', 'negative', '0', 'false'):
                        is_pos = False
                    else:
                        is_pos = el.startswith('pos')
                else:
                    is_pos = (e == 1)
            elif 'clk' in row:
                c = row['clk']
                if prev_clk is None:
                    if c == 1:
                        is_pos = True
                else:
                    if prev_clk == 0 and c == 1:
                        is_pos = True
                prev_clk = c
            else:
                is_pos = True
        else:
            is_pos = True
        results.append({
            'ciphertext': ciphertext_reg & 0x7FFF,
            'done': 1 if state == 3 else 0
        })
        if is_pos:
            if isinstance(row, dict):
                reset = int(row.get('reset', 0)) & 1
                start = int(row.get('start', 0)) & 1
                plaintext = int(row.get('plaintext', 0)) & 0x7FFF
                key = int(row.get('key', 0)) & ((1 << 45) - 1)
            else:
                reset = start = plaintext = key = 0
            if reset:
                state = 0
                plaintext_reg = 0
                key_reg = 0
                sums = [0, 0, 0]
                ciphertext_reg = 0
            else:
                if state == 0:
                    if start:
                        plaintext_reg = plaintext
                        key_reg = key
                        state = 1
                elif state == 1:
                    p0 = plaintext_reg & 0x1F
                    p1 = (plaintext_reg >> 5) & 0x1F
                    p2 = (plaintext_reg >> 10) & 0x1F
                    k = [(key_reg >> (5 * i)) & 0x1F for i in range(9)]
                    sums[0] = p0 * k[0] + p1 * k[1] + p2 * k[2]
                    sums[1] = p0 * k[3] + p1 * k[4] + p2 * k[5]
                    sums[2] = p0 * k[6] + p1 * k[7] + p2 * k[8]
                    state = 2
                elif state == 2:
                    c0 = sums[0] % 26
                    c1 = sums[1] % 26
                    c2 = sums[2] % 26
                    ciphertext_reg = (c0 & 0x1F) | ((c1 & 0x1F) << 5) | ((c2 & 0x1F) << 10)
                    state = 3
                elif state == 3:
                    state = 0
    return results

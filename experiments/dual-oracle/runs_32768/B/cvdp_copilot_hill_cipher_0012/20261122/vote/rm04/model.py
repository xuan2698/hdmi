def reference(vectors):
    IDLE, COMPUTE, COMPUTE_MOD, DONE = 0, 1, 2, 3
    state = IDLE
    cipher_reg = 0
    reset = 0
    start = 0
    plaintext = 0
    key = 0
    prev_clk = 0
    result = []

    for idx, row in enumerate(vectors):
        if isinstance(row, dict):
            if "reset" in row:
                reset = row["reset"]
            if "start" in row:
                start = row["start"]
            if "plaintext" in row:
                plaintext = row["plaintext"]
            if "key" in row:
                key = row["key"]

        reset_i = int(reset) if reset is not None else 0
        start_i = int(start) if start is not None else 0
        plaintext_i = int(plaintext) if plaintext is not None else 0
        key_i = int(key) if key is not None else 0

        posedge = False
        if isinstance(row, dict):
            handled = False
            if "edge" in row:
                e = row["edge"]
                handled = True
            elif "clk_edge" in row:
                e = row["clk_edge"]
                handled = True
            elif "edge_type" in row:
                e = row["edge_type"]
                handled = True
            elif "posedge" in row:
                posedge = bool(row["posedge"])
                handled = True
            elif "negedge" in row:
                posedge = not bool(row["negedge"])
                handled = True
            elif "clk" in row:
                clk = int(row["clk"])
                if idx == 0:
                    posedge = (clk == 1)
                else:
                    posedge = (prev_clk == 0 and clk == 1)
                prev_clk = clk
                handled = True

            if handled and ("edge" in row or "clk_edge" in row or "edge_type" in row):
                if isinstance(e, str):
                    s = e.lower()
                    if "pos" in s or "rise" in s:
                        posedge = True
                    elif "neg" in s or "fall" in s:
                        posedge = False
                    else:
                        posedge = bool(int(s)) if s.isdigit() else (idx % 2 == 0)
                else:
                    posedge = bool(e)
            elif not handled:
                posedge = (idx % 2 == 0)
        else:
            posedge = (idx % 2 == 0)

        done_now = 1 if state == DONE else 0
        result.append({"ciphertext": cipher_reg, "done": done_now})

        if posedge:
            if reset_i:
                state = IDLE
                cipher_reg = 0
            else:
                if state == IDLE:
                    if start_i:
                        state = COMPUTE
                elif state == COMPUTE:
                    state = COMPUTE_MOD
                elif state == COMPUTE_MOD:
                    p0 = plaintext_i & 31
                    p1 = (plaintext_i >> 5) & 31
                    p2 = (plaintext_i >> 10) & 31

                    k0 = key_i & 31
                    k1 = (key_i >> 5) & 31
                    k2 = (key_i >> 10) & 31
                    k3 = (key_i >> 15) & 31
                    k4 = (key_i >> 20) & 31
                    k5 = (key_i >> 25) & 31
                    k6 = (key_i >> 30) & 31
                    k7 = (key_i >> 35) & 31
                    k8 = (key_i >> 40) & 31

                    c0 = (p0 * k0 + p1 * k1 + p2 * k2) % 26
                    c1 = (p0 * k3 + p1 * k4 + p2 * k5) % 26
                    c2 = (p0 * k6 + p1 * k7 + p2 * k8) % 26

                    cipher_reg = c0 | (c1 << 5) | (c2 << 10)
                    state = DONE
                elif state == DONE:
                    state = IDLE

    return result

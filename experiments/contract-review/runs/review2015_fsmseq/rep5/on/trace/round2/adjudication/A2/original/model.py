def reference(vectors):
    # R_RESET_CLEAR: synchronous reset forces state S0 and start_shifting=0 on the settled edge.
    # R_SET_OR_HOLD_1101: detection of 1101 sets start_shifting=1 and FOUND holds it until reset.
    # R_KEEP_ZERO_UNTIL_FOUND: start_shifting remains 0 before detection.
    state = 0  # S0
    out = []
    for row in vectors:
        reset = row['reset']
        data = row['data']
        if reset == 1:
            nxt = 0  # S0
        else:
            if state == 0:  # S0
                if data == 1:
                    nxt = 1  # S1
                else:
                    nxt = 0  # S0
            elif state == 1:  # S1
                if data == 1:
                    nxt = 2  # S11
                else:
                    nxt = 0  # S0
            elif state == 2:  # S11
                if data == 1:
                    nxt = 2  # S11 (overlapping 1s)
                else:
                    nxt = 3  # S110
            elif state == 3:  # S110
                if data == 1:
                    nxt = 4  # FOUND
                else:
                    nxt = 0  # S0
            else:  # state == 4, FOUND
                nxt = 4
        state = nxt
        if state == 4:
            start_shifting = 1
        else:
            start_shifting = 0
        out.append({'start_shifting': start_shifting})
    return out

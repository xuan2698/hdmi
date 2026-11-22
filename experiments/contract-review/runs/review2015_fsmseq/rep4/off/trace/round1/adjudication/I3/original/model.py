def reference(vectors):
    # FSM states
    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4
    state = S0
    start_shifting = 0
    out = []

    for vec in vectors:
        reset = vec.get('reset', 0) & 1
        data = vec.get('data', 0) & 1

        # R1: synchronous active-high reset forces start_shifting=0 (priority 1)
        if reset == 1:
            state = S0
            start_shifting = 0
        else:
            # Compute next state from current state and data
            if state == S0:
                nxt = S1 if data == 1 else S0
            elif state == S1:
                nxt = S2 if data == 1 else S0
            elif state == S2:
                nxt = S3 if data == 0 else S2
            elif state == S3:
                nxt = S4 if data == 1 else S1
            else:  # S4
                nxt = S4

            # R2: already in S4, latch stays 1 (priority 2)
            # R3: transition into S4 sets start_shifting=1 (priority 3)
            # R4: otherwise start_shifting stays 0 (priority 4)
            if state == S4:
                start_shifting = 1  # R2
            elif nxt == S4:
                start_shifting = 1  # R3
            else:
                start_shifting = 0  # R4

            state = nxt

        out.append({'start_shifting': start_shifting & 1})

    return out

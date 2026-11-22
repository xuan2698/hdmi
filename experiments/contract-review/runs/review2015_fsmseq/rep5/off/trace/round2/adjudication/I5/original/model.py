def reference(vectors):
    # FSM states
    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4
    state = S0
    start_shifting = 0
    out = []

    for row in vectors:
        reset = row.get('reset', 0) & 1
        data = row.get('data', 0) & 1

        # R1: reset == 1 -> start_shifting = 0, state = S0 (sync, same cycle)
        if reset == 1:
            state = S0
            start_shifting = 0
            out.append({'start_shifting': start_shifting})
            continue

        # Compute next state from current state and data
        if state == S0:
            nxt = S1 if data == 1 else S0
        elif state == S1:
            nxt = S2 if data == 1 else S0
        elif state == S2:
            nxt = S3 if data == 0 else S2
        elif state == S3:
            nxt = S4 if data == 1 else S0
        else:  # S4
            nxt = S4

        # R2/R5: state == S4 -> start_shifting stays 1
        # R3: state == S3 and data == 1 -> next_state == S4 -> start_shifting = 1
        # R4: otherwise start_shifting = 0
        if state == S4:
            start_shifting = 1  # R2, R5
        elif nxt == S4:
            start_shifting = 1  # R3
        else:
            start_shifting = 0  # R4

        state = nxt
        out.append({'start_shifting': start_shifting})

    return out

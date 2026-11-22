def reference(vectors):
    # FSM states
    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4

    # Power-up state (unspecified, but we pick S0)
    state = S0
    start_shifting = 0

    results = []

    for vec in vectors:
        reset = vec.get('reset', 0) & 1
        data = vec.get('data', 0) & 1

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

        # R1: reset == 1 -> start_shifting = 0 (priority 1)
        if reset == 1:
            start_shifting = 0
            state = S0
        else:
            # R2: state == S4 -> start_shifting = 1 (priority 2)
            if state == S4:
                start_shifting = 1
            # R3: next_state == S4 -> start_shifting = 1 (priority 3)
            elif nxt == S4:
                start_shifting = 1
            # R4: otherwise start_shifting = 0 (priority 4)
            else:
                start_shifting = 0
            state = nxt

        results.append({'start_shifting': start_shifting & 1})

    return results

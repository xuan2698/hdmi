def reference(vectors):
    # State encoding
    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4

    # Initialize state to S0 (power-up)
    state = S0
    start_shifting = 0

    results = []

    for vec in vectors:
        reset = vec.get('reset', 0) & 1
        data = vec.get('data', 0) & 1

        # Compute next state based on current state and data
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
            state = S0
            start_shifting = 0
        else:
            # R2: state == S4 -> start_shifting = 1 (priority 2)
            # R3: next_state == S4 -> start_shifting = 1 (priority 3)
            # R4: otherwise -> start_shifting = 0 (priority 4)
            if state == S4:
                start_shifting = 1
            elif nxt == S4:
                start_shifting = 1
            else:
                start_shifting = 0
            state = nxt

        results.append({'start_shifting': start_shifting & 1})

    return results

def reference(vectors):
    # State encoding
    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4

    # Initialize state and output
    state = S0
    start_shifting = 0

    results = []

    for vec in vectors:
        reset = vec.get('reset', 0)
        data = vec.get('data', 0)

        # R1: synchronous reset, priority 1
        if reset == 1:
            state = S0
            start_shifting = 0
        else:
            # Compute next state based on current state and data
            if state == S0:
                next_state = S1 if data == 1 else S0
            elif state == S1:
                next_state = S2 if data == 1 else S0
            elif state == S2:
                next_state = S3 if data == 0 else S2
            elif state == S3:
                next_state = S4 if data == 1 else S0
            else:  # S4
                next_state = S4

            # R2: state == S4 -> start_shifting stays 1
            # R3: state == S3 and data == 1 -> start_shifting asserts same cycle
            # R4: otherwise start_shifting stays 0 (unless already latched)
            if state == S4:
                start_shifting = 1
            elif state == S3 and data == 1:
                start_shifting = 1
            else:
                start_shifting = 0

            state = next_state

        results.append({'start_shifting': start_shifting})

    return results

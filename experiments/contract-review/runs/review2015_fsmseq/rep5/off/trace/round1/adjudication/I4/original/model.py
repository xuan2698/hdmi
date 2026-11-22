def reference(vectors):
    # State encoding
    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4

    # Power-up state (unspecified in spec; choose S0)
    state = S0
    start_shifting = 0

    results = []

    for vec in vectors:
        reset = vec.get('reset', 0) & 1
        data = vec.get('data', 0) & 1

        # Compute next state and next output based on current state and inputs
        # R1: reset == 1 -> start_shifting = 0, state -> S0
        if reset == 1:
            next_state = S0
            next_start_shifting = 0  # R1
        else:
            # Transition logic
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

            # Output logic
            if state == S4:
                next_start_shifting = 1  # R2
            elif state == S3 and data == 1:
                next_start_shifting = 1  # R3 (visible next cycle)
            else:
                next_start_shifting = 0  # R4

        # Sample after posedge: outputs reflect the registered value
        # R3 says visible next_cycle, so start_shifting output this cycle
        # reflects the value latched at the previous edge.
        results.append({'start_shifting': start_shifting})

        # Update registers at posedge
        state = next_state
        start_shifting = next_start_shifting

    return results

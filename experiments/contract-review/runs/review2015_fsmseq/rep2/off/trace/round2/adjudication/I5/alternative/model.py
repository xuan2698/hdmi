def reference(vectors):
    # FSM states
    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4

    # State registers (initialized to S0 at power-up)
    state = S0
    start_shifting = 0

    results = []

    for vec in vectors:
        reset = vec.get('reset', 0) & 1
        data = vec.get('data', 0) & 1

        # --- Compute next state and next start_shifting based on current state ---
        # R1: reset == 1 -> start_shifting = 0 (sync reset, priority 1)
        # R2: reset == 0 and state == S4 -> start_shifting = 1 (priority 2)
        # R3: reset == 0 and state == S3 and data == 1 -> start_shifting = 1 (priority 3)
        # R4: reset == 0 and not S4 and not (S3 and data==1) -> start_shifting = 0 (priority 4)
        # Interpretation: start_shifting is registered (next_cycle visibility),
        # so the value sampled at this posedge reflects the PREVIOUS state's decision.
        # We compute the new value that will be visible on the NEXT posedge.

        if reset == 1:
            # R1: sync reset
            next_state = S0
            next_start_shifting = 0
        else:
            # Determine next state based on current state and data
            if state == S0:
                next_state = S1 if data == 1 else S0
            elif state == S1:
                next_state = S2 if data == 1 else S0
            elif state == S2:
                next_state = S3 if data == 0 else S2
            elif state == S3:
                next_state = S4 if data == 1 else S0
            else:  # S4
                next_state = S4  # latched

            # Determine next start_shifting (registered, next_cycle visibility)
            # R2: state == S4 -> 1
            # R3: state == S3 and data == 1 -> 1
            # R4: otherwise -> 0
            if state == S4:
                next_start_shifting = 1  # R2
            elif state == S3 and data == 1:
                next_start_shifting = 1  # R3
            else:
                next_start_shifting = 0  # R4

        # Output visible at this posedge = current registered value (before update)
        results.append({'start_shifting': start_shifting})

        # Update registers for next cycle
        state = next_state
        start_shifting = next_start_shifting

    return results

def reference(vectors):
    # State encoding
    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4

    # Power-up state (unspecified, but we pick S0)
    state = S0
    start_shifting = 0

    results = []

    for vec in vectors:
        reset = vec.get('reset', 0) & 1
        data = vec.get('data', 0) & 1

        # Compute next state and next output based on current state and inputs
        if reset == 1:
            # R1: reset == 1 -> start_shifting = 0, state -> S0
            next_state = S0
            next_start_shifting = 0
        else:
            # Determine next state from current state and data
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

            # R2: reset == 0 and state == S4 -> start_shifting = 1
            # R3: reset == 0 and state != S4 and next_state == S4 -> start_shifting = 1 (next_cycle visible)
            # R4: reset == 0 and state != S4 and next_state != S4 -> start_shifting = 0
            if state == S4:
                next_start_shifting = 1  # R2
            elif next_state == S4:
                next_start_shifting = 1  # R3 (visible next cycle)
            else:
                next_start_shifting = 0  # R4

        # Output visible this cycle is the value latched at this posedge
        # For R3, the spec says visible "next_cycle", meaning the output
        # becomes 1 on the cycle AFTER the transition into S4.
        # So we output the CURRENT start_shifting (before update) for this cycle,
        # then update state and start_shifting for next cycle.
        results.append({'start_shifting': start_shifting & 1})

        # Update state and output for next cycle
        state = next_state
        start_shifting = next_start_shifting

    return results

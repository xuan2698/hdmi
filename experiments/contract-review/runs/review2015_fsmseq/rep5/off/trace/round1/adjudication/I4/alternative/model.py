def reference(vectors):
    # State encoding
    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4

    # Power-up state (unspecified; choose S0, start_shifting=0)
    state = S0
    start_shifting = 0

    results = []

    for vec in vectors:
        reset = vec.get('reset', 0) & 1
        data = vec.get('data', 0) & 1

        # Compute next state and next start_shifting based on current state
        # and inputs (sampled at posedge).
        if reset == 1:
            # R1: synchronous reset, priority 1
            next_state = S0
            next_start_shifting = 0
        else:
            if state == S4:
                # R2: once in S4, stay and keep start_shifting=1
                next_state = S4
                next_start_shifting = 1
            else:
                # Compute next state from current state and data
                if state == S0:
                    next_state = S1 if data == 1 else S0
                elif state == S1:
                    next_state = S2 if data == 1 else S0
                elif state == S2:
                    next_state = S3 if data == 0 else S2
                elif state == S3:
                    next_state = S4 if data == 1 else S0
                else:
                    next_state = S0

                if next_state == S4:
                    # R3: transition into S4 sets start_shifting visible next cycle
                    next_start_shifting = 0
                else:
                    # R4: no match, start_shifting stays 0
                    next_start_shifting = 0

        # Output visible this cycle is the registered value (from previous edge)
        results.append({'start_shifting': start_shifting})

        # Update registers at posedge
        state = next_state
        start_shifting = next_start_shifting

    return results

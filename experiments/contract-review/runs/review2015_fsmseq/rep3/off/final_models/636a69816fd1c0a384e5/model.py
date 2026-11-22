def reference(vectors):
    # FSM states
    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4

    # State registers (power-up unspecified -> default to S0)
    state = S0
    start_shifting = 0

    results = []

    for vec in vectors:
        reset = vec.get('reset', 0) & 1
        data = vec.get('data', 0) & 1

        # --- Sample phase: compute next state and outputs based on current state ---
        # R1: reset == 1 -> start_shifting = 0 (priority 1)
        # R2: reset == 0 and state == S4 -> start_shifting = 1 (priority 2)
        # R3: reset == 0 and state == S4 -> start_shifting = 1 (priority 3, same as R2)
        # R4: reset == 0 and state != S4 -> start_shifting = 0 (priority 4)
        if reset == 1:
            # R1
            next_start_shifting = 0
            next_state = S0
        else:
            if state == S4:
                # R2 / R3: latched high forever until reset
                next_start_shifting = 1
                next_state = S4
            else:
                # R4: still searching
                next_start_shifting = 0
                # Transition logic for sequence 1101
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

        # Output visible same_cycle (based on current state / reset)
        # R1: reset==1 -> 0
        # R2: reset==0 and state==S4 -> 1
        # R4: reset==0 and state!=S4 -> 0
        if reset == 1:
            out = 0  # R1
        elif state == S4:
            out = 1  # R2
        else:
            out = 0  # R4

        results.append({'start_shifting': out})

        # --- Update phase (posedge) ---
        state = next_state
        start_shifting = next_start_shifting

    return results

def reference(vectors):
    # State encoding
    A, B, C, D = 0, 1, 2, 3
    state = A  # power-up state (unspecified, but reset will handle)

    results = []
    for vec in vectors:
        reset = vec.get('reset', 0)
        inp = vec.get('in', 0)

        # R_RESET: synchronous active high reset -> state A (priority 0)
        # R_TRANS: next state determined by table on posedge when reset == 0
        # Compute next state based on current state and input
        if reset == 1:
            next_state = A
        else:
            if state == A:
                next_state = A if inp == 0 else B
            elif state == B:
                next_state = C if inp == 0 else B
            elif state == C:
                next_state = A if inp == 0 else D
            else:  # state == D
                next_state = C if inp == 0 else B

        # R_A / R_B / R_C / R_D: combinational output based on current state
        # Output is visible same cycle (Moore output from current state)
        if state == D:
            out = 1
        else:
            out = 0

        results.append({'out': out})

        # Advance state at posedge (after sampling)
        state = next_state

    return results

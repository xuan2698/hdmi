def reference(vectors):
    # Contract rules implemented:
    # R1: reset == 1 -> start_shifting = 0 (sync, same cycle, priority 1)
    # R2: reset == 0 and state == S4 -> start_shifting = 1 (priority 2)
    # R3: reset == 0 and state == S3 and data == 1 -> start_shifting = 1 (priority 3)
    # R4: reset == 0 and state != S4 and not (state == S3 and data == 1) -> start_shifting = 0 (priority 4)
    #
    # State machine (posedge updates):
    # S0: no prefix matched
    # S1: matched '1'
    # S2: matched '11'
    # S3: matched '110'
    # S4: matched '1101' (latched forever until reset)
    #
    # Outputs are computed combinationally from current state and inputs
    # (visible same_cycle), then state updates on posedge.

    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4

    state = S0
    results = []

    for vec in vectors:
        reset = vec.get('reset', 0) & 1
        data = vec.get('data', 0) & 1

        # Compute output for this cycle (same_cycle visibility)
        if reset == 1:
            # R1
            start_shifting = 0
        elif state == S4:
            # R2
            start_shifting = 1
        elif state == S3 and data == 1:
            # R3
            start_shifting = 1
        else:
            # R4
            start_shifting = 0

        results.append({'start_shifting': start_shifting})

        # State update on posedge (after sampling)
        if reset == 1:
            state = S0
        else:
            if state == S0:
                state = S1 if data == 1 else S0
            elif state == S1:
                state = S2 if data == 1 else S0
            elif state == S2:
                state = S3 if data == 0 else S2
            elif state == S3:
                state = S4 if data == 1 else S0
            elif state == S4:
                state = S4

    return results

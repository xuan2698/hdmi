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

        # R1: Reset is active high synchronous; on reset, output 0 and state S0
        if reset == 1:
            # R1: reset == 1 -> start_shifting = 0 (same_cycle, priority 1)
            start_shifting = 0
            state = S0
            results.append({'start_shifting': start_shifting})
            continue

        # R2: reset == 0 and state == S4 -> start_shifting = 1 (priority 2)
        # R3: reset == 0 and state == S3 and data == 1 -> start_shifting = 1 (priority 3)
        # R4: reset == 0 and state != S4 and not (state == S3 and data == 1) -> start_shifting = 0 (priority 4)
        # R5: reset == 0 -> covered by above
        if state == S4:
            # R2: latch high forever until reset
            start_shifting = 1
        elif state == S3 and data == 1:
            # R3: completing bit detected; assert same_cycle (selected interpretation)
            start_shifting = 1
        else:
            # R4: no completion
            start_shifting = 0

        # State transition (posedge, after sampling)
        if state == S0:
            if data == 1:
                state = S1
            else:
                state = S0
        elif state == S1:
            if data == 1:
                state = S2
            else:
                state = S0
        elif state == S2:
            if data == 0:
                state = S3
            else:
                state = S2
        elif state == S3:
            if data == 1:
                state = S4
            else:
                state = S0
        elif state == S4:
            state = S4

        results.append({'start_shifting': start_shifting})

    return results

def reference(vectors):
    # Contract rules:
    # R1: reset == 1 -> start_shifting = 0 (sync reset, same cycle)
    # R2: reset == 0 and state == S4 -> start_shifting = 1 (latched)
    # R3: reset == 0 and state == S3 and data == 1 -> start_shifting = 1
    # R4: reset == 0 and not S4 and not (S3 and data==1) -> start_shifting = 0
    # R5: same as R3 but next_cycle visibility (state transition)
    # Uncertain: latch interpretation chosen (FSM stays in S4 forever after match)

    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4
    state = S0
    start_shifting = 0
    out = []

    for row in vectors:
        reset = row.get('reset', 0) & 1
        data = row.get('data', 0) & 1

        # Compute outputs visible same cycle (based on current state and inputs)
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

        out.append({'start_shifting': start_shifting & 1})

        # State update at posedge (after sampling)
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
                if data == 1:
                    state = S4  # R5
                else:
                    state = S0
            elif state == S4:
                state = S4  # latch interpretation

    return out

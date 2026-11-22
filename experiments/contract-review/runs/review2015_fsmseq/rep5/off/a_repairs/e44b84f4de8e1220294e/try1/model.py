def reference(vectors):
    # Contract rules implemented below.
    # R1: reset == 1 -> start_shifting = 0 (sync, priority 1)
    # R2/R5: reset == 0 and state == S4 -> start_shifting = 1 (priority 2)
    # R3: reset == 0 and state == S3 and data == 1 -> start_shifting = 1 (priority 3)
    # R4: otherwise start_shifting = 0 (priority 4)
    # State machine: S0 (none), S1 ('1'), S2 ('11'), S3 ('110'), S4 ('1101' latched)
    # Output is combinational on current state and current data (visible same_cycle).
    # State updates on posedge using current inputs.

    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4
    state = S0
    out = []

    for row in vectors:
        reset = row.get('reset', 0) & 1
        data = row.get('data', 0) & 1

        # Compute next state from current state and data
        if state == S0:
            nxt = S1 if data == 1 else S0
        elif state == S1:
            nxt = S2 if data == 1 else S0
        elif state == S2:
            nxt = S3 if data == 0 else S2
        elif state == S3:
            nxt = S4 if data == 1 else S0
        else:  # S4
            nxt = S4

        # R1: reset high -> output 0, state goes to S0
        if reset == 1:
            start_shifting = 0
            state = S0
        else:
            # R2/R5: already latched
            if state == S4:
                start_shifting = 1
            # R3: transition into S4 this cycle
            elif nxt == S4:
                start_shifting = 1
            # R4: otherwise 0
            else:
                start_shifting = 0
            state = nxt

        out.append({'start_shifting': start_shifting & 1})

    return out

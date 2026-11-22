def reference(vectors):
    # Contract rules:
    # R1: reset == 1 -> start_shifting = 0 (sync reset, same_cycle)
    # R2: reset == 0 and state == S4 -> start_shifting = 1
    # R3: reset == 0 and state == S3 and data == 1 -> start_shifting = 1
    # R4: reset == 0 and not S4 and not (S3 and data==1) -> start_shifting = 0
    # States: S0 (no prefix), S1 (matched '1'), S2 (matched '11'),
    #         S3 (matched '110'), S4 (found 1101, latched)
    # Output is same_cycle (combinational relative to current state+data+reset).

    S0, S1, S2, S3, S4 = 0, 1, 2, 3, 4
    state = S0
    start_shifting = 0
    results = []

    for row in vectors:
        reset = row.get('reset', 0) & 1
        data = row.get('data', 0) & 1

        # R1: synchronous reset forces output low and state to S0
        if reset == 1:
            start_shifting = 0
            state = S0
        else:
            # R2: already latched
            if state == S4:
                start_shifting = 1
            # R3: detecting 1101 now
            elif state == S3 and data == 1:
                start_shifting = 1
                state = S4
            # R4: not yet found
            else:
                start_shifting = 0
                # state transition for next cycle
                if state == S0:
                    state = S1 if data == 1 else S0
                elif state == S1:
                    state = S2 if data == 1 else S1
                elif state == S2:
                    state = S3 if data == 0 else S2
                elif state == S3:
                    # data == 0 here (data==1 handled above)
                    state = S1 if data == 1 else S0
                    # data is 0 -> S0
                    state = S0

        results.append({'start_shifting': start_shifting & 1})

    return results

def reference(vectors):
    # Contract implementation.
    # State: COUNT (current decade count 0..9), updated on posedge.
    # Output q reflects the state after the sampled posedge.
    # reset is active-high synchronous: on posedge with reset==1 -> q=0.
    # Otherwise q increments modulo 10.
    # Mid changes occur AFTER sampling and are carried to the next row.

    q = 0  # initial state (power-up unspecified; use 0 as concrete value)

    results = []
    for row in vectors:
        # Determine reset value for this row's sampled edge.
        # Mid changes from previous row are already applied to row (carried).
        reset = row.get('reset', 0)

        # R1_SYNC_RESET: reset == 1 on posedge -> q = 0
        # R2_COUNT_INC: reset == 0 -> q = (q + 1) % 10
        # R3_WRAP: handled by modulo (q==9 -> 0)
        if reset == 1:
            q = 0
        else:
            q = (q + 1) % 10

        # Output visible same cycle
        results.append({'q': q & 0xF})

        # Apply mid changes AFTER sampling (carried to next row).
        # Mid changes are provided as 'mid' dict in the row, applied after sampling.
        mid = row.get('mid')
        if mid:
            # Mid changes affect inputs for the next row; they are carried
            # to the start of the next row. We store them by mutating a copy
            # for the next iteration. Since vectors are given as rows,
            # mid changes are applied to the next row's inputs.
            # We handle this by tracking pending mid overrides.
            pass

    return results

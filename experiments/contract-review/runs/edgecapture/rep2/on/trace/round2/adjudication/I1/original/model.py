def reference(vectors):
    # 32-bit mask for the out and in vectors.
    mask = (1 << 32) - 1

    # State initialization: out is the sticky capture register; prev_in is the previous sampled input.
    state_out = 0
    prev_in = 0

    # Carried input values for the next row.  A row's explicit reset/in overrides these before the edge,
    # and any mid changes update them after the edge for the next row.
    current_reset = 0
    current_in = 0

    result = []

    for idx in range(len(vectors)):
        row = vectors[idx]

        # Drive this row's inputs before the sampled posedge.  If a field is absent, the carried value remains.
        if "reset" in row:
            current_reset = row["reset"]
        if "in" in row:
            current_in = row["in"]

        current_in = current_in & mask
        current_reset = 1 if current_reset else 0

        # Rule reset_clear (priority 2): synchronous active-high reset clears out on this posedge.
        # Rule capture_fall (priority 1): when reset is low, capture bits where prev_in was 1 and current in is 0.
        # Rule hold_state (priority 0): otherwise each out bit holds its previous value.
        if current_reset == 1:
            state_out = 0
        else:
            falls = prev_in & ((~current_in) & mask)
            state_out = (state_out | falls) & mask

        # State prev_in tracks the sampled in on every posedge, including reset cycles.
        prev_in = current_in & mask

        # Output is visible in the same cycle after the sampled edge.
        result.append({"out": state_out & mask})

        # Mid changes occur after sampling and before the next edge.  They become start values for the next row
        # unless that next row explicitly overrides the same input.
        mid = row.get("mid")
        if mid is not None:
            if "reset" in mid:
                current_reset = mid["reset"]
                current_reset = 1 if current_reset else 0
            if "in" in mid:
                current_in = mid["in"] & mask

    return result

def reference(vectors):
    # State: 3-bit counter q, initialized flag
    # Rule hold_when_a_high: on posedge, if initialized and a==1, hold q
    # Rule increment_when_a_low: on posedge, if prev_a==0, increment q (mod 8)
    # First posedge: q = 4 regardless of a (initialization)
    # mid changes: applied after sampling, carried to next row

    q = None  # unspecified before first posedge
    initialized = False
    prev_a = None  # previous a value (from prior row's sampled a, or mid change)

    results = []
    for row in vectors:
        a = row['a']
        # At posedge: sample using prev_a (the a value carried from before this edge)
        # Determine effective a for this edge: prev_a if set, else current a
        # Actually: each row's values are driven before the sampled edge.
        # prev_a is the a from the previous row (or mid change), which is the value
        # present at the start of this row before the edge.
        # The row's 'a' is driven before the edge, so it IS the value at the edge.
        # But mid changes occur AFTER sampling, before the other edge, carried to next row.
        # So: the a used at this posedge is the row's a, unless a mid change from
        # the previous row overrode it. Mid changes are "carried to the start of the next row".
        # So effective_a = mid_a if mid_a is not None else row['a']
        # Wait - "Each row's values are driven before the sampled edge" means row['a']
        # is the value at the edge. But mid changes from previous row are carried to
        # start of next row, meaning they override row['a']? Let's re-read:
        # "Optional mid input changes occur AFTER sampling, before the other edge, and are
        # carried to the start of the next row."
        # So a mid change sets a new value that persists into the next row's start.
        # But the next row also drives its own 'a' before the edge... The mid change
        # is carried to the start, then the row's driven value applies before the edge.
        # Hmm, ambiguous. Given the contract, mid changes are optional and not present
        # in the given vectors (no mid field). So just use row['a'].

        effective_a = row['a']

        if not initialized:
            # First posedge: q = 4 regardless of a
            q = 4
            initialized = True
        else:
            # prev_a is the a value from the previous cycle (the one that was
            # sampled at the previous posedge, i.e., the previous row's effective_a)
            if prev_a == 0:
                q = (q + 1) % 8
            else:
                # prev_a == 1: hold
                q = q

        results.append({'q': q})

        # After sampling, update prev_a for next cycle
        prev_a = effective_a

        # Handle mid changes if present (after sampling, before next edge)
        if 'mid' in row and row['mid'] is not None:
            mid = row['mid']
            if 'a' in mid:
                prev_a = mid['a']

    return results

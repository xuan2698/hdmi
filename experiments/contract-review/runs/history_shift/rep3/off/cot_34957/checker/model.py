def reference(vectors):
    out = []
    state = 0
    for row in vectors:
        # Apply mid changes that occur after sampling but before next edge
        # (mid changes are carried to the start of the next row)
        # We process them at the end of the row.
        clk = row.get('clk', 0)
        areset = row.get('areset', 0)
        predict_valid = row.get('predict_valid', 0)
        predict_taken = row.get('predict_taken', 0)
        train_mispredicted = row.get('train_mispredicted', 0)
        train_taken = row.get('train_taken', 0)
        train_history = row.get('train_history', 0)

        # Asynchronous reset: if areset is asserted, state becomes 0
        # (positive edge triggered asynchronous reset)
        if areset:
            state = 0

        # Sample after posedge has settled: compute next state on posedge
        # We treat the row as the values driven before the sampled edge.
        # The clock edge triggers the update.
        if clk:
            if train_mispredicted:
                # Misprediction takes precedence
                state = ((train_history << 1) | train_taken) & 0xFFFFFFFF
            elif predict_valid:
                state = ((state << 1) | predict_taken) & 0xFFFFFFFF

        # Output is the current value of the branch history register
        out.append({'predict_history': state & 0xFFFFFFFF})

        # Process mid changes (after sampling, before other edge)
        # These are carried to the start of the next row.
        # Mid changes may include areset, predict_valid, etc.
        # We apply them to state for the next row's starting point.
        mid = row.get('mid', {})
        if mid:
            if mid.get('areset', 0):
                state = 0
            # Note: mid changes to control signals don't affect state directly
            # unless they cause a clock edge, which is handled by the next row's clk.
            # However, mid changes to areset are asynchronous and take effect immediately.
            # We already handled areset above for the row's own areset.
            # For mid areset, apply it now.
            if mid.get('areset', 0):
                state = 0

    return out

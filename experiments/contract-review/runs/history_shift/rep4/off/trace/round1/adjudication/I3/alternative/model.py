def reference(vectors):
    # Contract implementation.
    # State: history (32-bit global branch history shift register).
    # Bit 0 is the youngest branch direction.
    #
    # R1_async_reset: areset == 1 -> predict_history = 0 (asynchronous, same cycle).
    # R2_mispredict_load: areset == 0 && train_mispredicted == 1 ->
    #     history <= {train_taken, train_history[31:1]}  (candidate interpretation)
    #     (train_taken as MSB, train_history shifted right)
    #     visible next cycle.
    # R3_predict_shift: areset == 0 && train_mispredicted == 0 && predict_valid == 1 ->
    #     history <= {history[30:0], predict_taken}  (shift in predict_taken at LSB)
    #     visible next cycle.
    # R4_hold: areset == 0 && train_mispredicted == 0 && predict_valid == 0 ->
    #     history unchanged.
    #
    # Misprediction takes precedence over prediction when both occur.
    # Mid input changes occur AFTER sampling, before the other edge,
    # and are carried to the start of the next row.

    history = 0  # power-up unspecified; use 0 as concrete value
    results = []

    for row in vectors:
        areset = row.get('areset', 0) & 1
        predict_valid = row.get('predict_valid', 0) & 1
        predict_taken = row.get('predict_taken', 0) & 1
        train_mispredicted = row.get('train_mispredicted', 0) & 1
        train_taken = row.get('train_taken', 0) & 1
        train_history = row.get('train_history', 0) & 0xFFFFFFFF

        # R1_async_reset: asynchronous reset, visible same cycle.
        if areset:
            history = 0
            results.append({'predict_history': history & 0xFFFFFFFF})
            # mid changes after sampling: none affect state here since reset dominates
            continue

        # Compute next state at posedge (visible next cycle).
        if train_mispredicted:
            # R2_mispredict_load (candidate interpretation):
            # loaded history = {train_taken, train_history[31:1]}
            next_history = ((train_taken & 1) << 31) | ((train_history >> 1) & 0x7FFFFFFF)
        elif predict_valid:
            # R3_predict_shift: shift in predict_taken at LSB.
            next_history = ((history << 1) & 0xFFFFFFFE) | (predict_taken & 1)
        else:
            # R4_hold
            next_history = history

        # Output is current history value (before this edge's update).
        results.append({'predict_history': history & 0xFFFFFFFF})

        # Apply posedge update.
        history = next_history & 0xFFFFFFFF

    return results

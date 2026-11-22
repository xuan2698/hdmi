def reference(vectors):
    # Contract implementation for 32-bit global branch history shift register.
    # State: history (32-bit), initialized to 0 at power-up.
    # Output: predict_history = current history value (combinational read of state).
    #
    # Timing model:
    #   - Each row's inputs are driven before the sampled posedge.
    #   - We sample after the posedge has settled -> compute next state from
    #     current inputs and current state, then output reflects the state
    #     visible in that cycle.
    #   - areset is asynchronous, active high: when areset==1, output is 0
    #     immediately (same cycle), and state is reset to 0.
    #   - Optional mid input changes occur AFTER sampling, before the other
    #     edge, and are carried to the start of the next row. Since our
    #     sampling is at the posedge, mid changes affect the NEXT row's
    #     inputs. We model this by applying mid changes to the input set
    #     used for the next row's evaluation.
    #
    # We interpret each vector row as the inputs present at the sampled
    # posedge. The output for that row is the state visible after that edge
    # has settled (i.e., the registered value). For async reset, the output
    # is 0 in the same cycle.

    history = 0  # 32-bit state, power-up value 0

    # We'll track "pending" input overrides from mid changes of the previous row.
    # Mid changes occur after sampling and are carried to the start of the next row.
    pending = None

    results = []

    for row in vectors:
        # Merge pending mid changes (from previous row) into this row's inputs.
        # Mid changes override the driven values for the next row.
        inputs = dict(row)
        if pending is not None:
            inputs.update(pending)
            pending = None

        areset = inputs.get('areset', 0) & 1
        predict_valid = inputs.get('predict_valid', 0) & 1
        predict_taken = inputs.get('predict_taken', 0) & 1
        train_mispredicted = inputs.get('train_mispredicted', 0) & 1
        train_taken = inputs.get('train_taken', 0) & 1
        train_history = inputs.get('train_history', 0) & 0xFFFFFFFF

        # R1_async_reset: areset==1 -> output 0 same cycle, state reset to 0.
        if areset:
            history = 0
            results.append({'predict_history': 0})
            # No mid changes specified in contract for this row; pending stays None.
            continue

        # Compute next state based on priority:
        # R2_mispredict_load (priority 1) > R3_predict_shift (priority 2) > R4_hold (priority 3)
        if train_mispredicted:
            # R2_mispredict_load: history = (train_history << 1 | train_taken) & 0xFFFFFFFF
            # "history before the mispredicted branch (train_history) concatenated
            #  with the actual result of the branch (train_taken)"
            # train_history is 32 bits; concatenating with 1 bit gives 33 bits,
            # but the register is 32 bits. The spec says "load the branch history
            # register with the history after the completion of the mispredicted
            # branch". This means the new history is train_history shifted left
            # by 1 with train_taken in LSB, truncated to 32 bits.
            next_history = ((train_history << 1) | train_taken) & 0xFFFFFFFF
        elif predict_valid:
            # R3_predict_shift: shift in predict_taken from LSB side.
            # predict_history[0] is the youngest branch, so shift left and
            # put predict_taken in bit 0.
            next_history = ((history << 1) | predict_taken) & 0xFFFFFFFF
        else:
            # R4_hold: keep history unchanged.
            next_history = history

        # Output for this cycle is the state visible after the edge settles.
        # Since we're sampling after the posedge, the registered update has
        # taken effect, so output = next_history.
        history = next_history
        results.append({'predict_history': history & 0xFFFFFFFF})

    return results

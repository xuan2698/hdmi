def reference(vectors):
    # Contract implementation.
    # State encoding: S0=0, S1=1, S2=2, S3=3, S4=4
    # Output start_shifting is registered (next_cycle) relative to detecting posedge,
    # but the contract's "visible":"same_cycle" rules are interpreted as: the output
    # value returned for a row reflects the state AFTER the posedge update of that row.
    # We model: sample inputs at posedge, compute next state, update state, then output
    # is derived from the updated state (registered output, visible same_cycle as the
    # post-edge state). This matches "set start_shifting to 1, forever, until reset"
    # with the output reflecting the post-edge state.

    state = 0  # S0
    start_shifting = 0
    out = []

    for row in vectors:
        reset = row.get('reset', 0) & 1
        data = row.get('data', 0) & 1

        # R1: reset == 1 -> synchronous reset, output 0, state S0
        if reset == 1:
            state = 0
            start_shifting = 0
            out.append({'start_shifting': start_shifting})
            continue

        # Compute next state based on current state and data (posedge update)
        if state == 4:  # S4: latched forever until reset
            # R2: state == S4 -> start_shifting stays 1
            next_state = 4
        elif state == 3:  # S3
            if data == 1:
                # R3: state == S3 and data == 1 -> sequence found
                next_state = 4
            else:
                # "110" + 0 -> suffix "0", no prefix match -> S0
                next_state = 0
        elif state == 2:  # S2: matched "11"
            if data == 1:
                next_state = 3
            else:
                next_state = 0
        elif state == 1:  # S1: matched "1"
            if data == 1:
                next_state = 2
            else:
                next_state = 0
        else:  # S0
            if data == 1:
                next_state = 1
            else:
                next_state = 0

        state = next_state

        # R2/R3/R4: output derived from post-edge state
        if state == 4:
            start_shifting = 1
        else:
            start_shifting = 0

        out.append({'start_shifting': start_shifting})

    return out

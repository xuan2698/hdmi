def reference(vectors):
    # State
    ghr = 0
    pht = [0] * 128  # 2-bit saturating counters, init 0

    out = []

    for v in vectors:
        # Optional mid changes are applied AFTER sampling, before next edge.
        # We'll process: sample outputs based on current state, then apply
        # clock edge updates (using pre-edge inputs), then apply mid changes.

        areset = v.get('areset', 0)
        predict_valid = v.get('predict_valid', 0)
        predict_pc = v.get('predict_pc', 0)
        train_valid = v.get('train_valid', 0)
        train_taken = v.get('train_taken', 0)
        train_mispredicted = v.get('train_mispredicted', 0)
        train_history = v.get('train_history', 0)
        train_pc = v.get('train_pc', 0)

        # Asynchronous reset: if areset is high, outputs reflect reset state
        if areset:
            # Reset state: ghr=0, pht all zero
            # Outputs computed from reset state
            if predict_valid:
                idx = (predict_pc ^ 0) & 0x7F
                ctr = 0
                predict_taken = (ctr >> 1) & 1
                predict_history = 0
            else:
                predict_taken = 0
                predict_history = 0
            out.append({'predict_taken': predict_taken, 'predict_history': predict_history})
            # Apply reset at edge (async, so state becomes reset)
            ghr = 0
            pht = [0] * 128
            # mid changes after sampling: apply them (they occur after edge)
            # mid changes are in v.get('mid', {}) - but spec says optional mid input changes
            # We'll handle mid if present
            mid = v.get('mid', None)
            if mid:
                # mid changes occur after sampling, before other edge; carried to next row
                # For simplicity, apply mid changes to state now (they affect next row)
                # But mid changes are inputs, not state. Actually mid changes are input changes
                # that occur after sampling. They affect the next row's inputs.
                # Since we process row by row with inputs given, mid changes would be
                # reflected in next row's inputs already. So we can ignore mid here.
                pass
            continue

        # Normal operation (no reset)
        # Compute prediction outputs based on current state (pre-edge)
        if predict_valid:
            idx = (predict_pc ^ ghr) & 0x7F
            ctr = pht[idx]
            predict_taken = (ctr >> 1) & 1
            predict_history = ghr
        else:
            predict_taken = 0
            predict_history = 0

        out.append({'predict_taken': predict_taken, 'predict_history': predict_history})

        # Now compute next state (at positive clock edge)
        # Training takes precedence for GHR update
        next_ghr = ghr
        next_pht = list(pht)

        # Training PHT update
        if train_valid:
            tidx = (train_pc ^ train_history) & 0x7F
            ctr = next_pht[tidx]
            if train_taken:
                if ctr < 3:
                    ctr += 1
            else:
                if ctr > 0:
                    ctr -= 1
            next_pht[tidx] = ctr

        # GHR update: training mispredicted recovery takes precedence over prediction
        if train_valid and train_mispredicted:
            # Recover GHR to state immediately after mispredicting branch
            # train_history is the history used for the branch; after branch completes,
            # new history = (train_history << 1) | train_taken, masked to 7 bits
            next_ghr = ((train_history << 1) | train_taken) & 0x7F
        elif predict_valid:
            # Update GHR for predicted branch (predicted taken)
            next_ghr = ((ghr << 1) | predict_taken) & 0x7F

        # Apply edge updates
        ghr = next_ghr
        pht = next_pht

        # mid changes after sampling - ignore as they affect next row inputs

    return out

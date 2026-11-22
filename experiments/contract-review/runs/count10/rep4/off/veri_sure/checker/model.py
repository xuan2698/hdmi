def reference(vectors):
    # Contract:
    # - clk posedge samples inputs; reset is active-high synchronous.
    # - q is a 4-bit decade counter 0..9, wrapping 9 -> 0.
    # - Output latency: q reflects the state after the sampled posedge.
    # - Each row: inputs are driven before the sampled edge.
    # - Mid changes occur AFTER sampling, before the other edge, and carry
    #   to the start of the next row.
    #
    # We model the counter state. For each row, we first apply any pending
    # mid changes from the previous row (already stored in current inputs),
    # then sample at the posedge, then apply mid changes for this row.
    #
    # The vectors format: list of rows, each row is a dict with keys
    # 'clk', 'reset', 'q' (expected output) and possibly 'mid' changes.
    # We must return a list of dicts with output 'q' per row.
    #
    # Since the exact vector schema isn't fully specified, we implement a
    # robust interpreter: each row may contain input values and optional
    # 'mid' dict of changes applied after sampling.

    state = 0  # power-up unspecified; we choose 0 as concrete value
    results = []

    for row in vectors:
        # Inputs for this row (driven before sampled edge)
        reset = row.get('reset', 0)
        # clk is assumed to have a posedge in this row (sampled edge)
        # Sample at posedge:
        if reset:
            state = 0
        else:
            if state == 9:
                state = 0
            else:
                state = state + 1
        # Output after posedge (latency 1 cycle means q reflects new state)
        results.append({'q': state & 0xF})

        # Apply mid changes AFTER sampling, before other edge,
        # carried to start of next row.
        mid = row.get('mid', {})
        if 'reset' in mid:
            # mid reset change affects next row's input
            # We store it by modifying a pending input for next row.
            # Since we read reset from row each iteration, we need to
            # propagate mid changes. We'll use a pending dict.
            pass
        # To handle mid changes properly, we need to carry them forward.
        # We'll restructure: maintain pending inputs.

    # The above simple loop doesn't handle mid changes carried forward.
    # Re-implement with pending inputs.

    state = 0
    results = []
    pending = {}  # input overrides carried from previous row's mid

    for row in vectors:
        # Merge pending mid changes into current inputs
        reset = row.get('reset', pending.get('reset', 0))
        # (clk not needed for logic beyond posedge assumption)

        # Sample at posedge
        if reset:
            state = 0
        else:
            if state == 9:
                state = 0
            else:
                state = state + 1

        results.append({'q': state & 0xF})

        # Apply mid changes after sampling, carry to next row
        mid = row.get('mid', {})
        pending = {}
        for k, v in mid.items():
            pending[k] = v

    return results

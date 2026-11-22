def reference(vectors):
    # Contract implementation.
    # R1: state <= a AND b on posedge (inferred from waveforms).
    # R2: q = state after posedge (registered output of flip-flop).
    # No reset; power-up state is unspecified -> treat as 0 for concreteness.
    # Mid input changes occur AFTER sampling, before the other edge, and are
    # carried to the start of the next row. We process each row's inputs as
    # driven before the sampled posedge; mid changes are applied after the
    # posedge sample and carried forward.

    state = 0  # power-up unspecified; concrete default 0
    q = 0      # registered output mirrors state after posedge

    results = []
    for row in vectors:
        # Inputs driven before the sampled posedge edge.
        a = row.get('a', 0)
        b = row.get('b', 0)

        # R1: state <= a AND b on posedge
        next_state = 1 if (a == 1 and b == 1) else 0
        state = next_state

        # R2: q = state after posedge (registered output of flip-flop)
        q = state

        # Mid changes (if any) occur AFTER sampling; carried to next row.
        # They do not affect this row's sampled outputs.
        # (No explicit mid fields in the provided vectors; nothing to apply.)

        results.append({'q': q & 1, 'state': state & 1})

    return results

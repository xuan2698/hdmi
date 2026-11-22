def reference(vectors):
    # Contract implementation.
    # R1: state <= a AND b on posedge (next_cycle). Power-up state unspecified -> treat as 0.
    # R2: q = state after posedge (registered output of flip-flop). q mirrors state.
    # No reset. Mid changes occur after sampling, before other edge, carried to next row.
    state = 0
    q = 0
    out = []
    for row in vectors:
        a = row.get('a', 0)
        b = row.get('b', 0)
        # R1: compute next state from current inputs (sampled at posedge)
        next_state = 1 if (a and b) else 0
        # R2: q reflects state after posedge
        state = next_state
        q = state
        out.append({'q': q, 'state': state})
    return out

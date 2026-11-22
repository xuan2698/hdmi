def reference(vectors):
    # Contract implementation.
    # R1: state is a single flip-flop updated on posedge clk to a AND b.
    # R2: q is combinational a AND b of current inputs (same cycle).
    # Reset: none. Power-up state unspecified -> use 0 as concrete value.
    state = 0
    out = []
    for v in vectors:
        a = v.get('a', 0) & 1
        b = v.get('b', 0) & 1
        # R2: combinational q = a AND b (same cycle)
        q = a & b
        # R1: state visible is the current flip-flop value (next_cycle semantics:
        # the sampled state reflects the value latched at the previous posedge).
        out.append({'q': q & 1, 'state': state & 1})
        # R1: posedge update: next state = a AND b
        state = a & b
    return out

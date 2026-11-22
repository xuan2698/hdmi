def reference(vectors):
    # Contract implementation.
    # R1: state updates to a & b on posedge clk (visible next cycle).
    # R2: q = a & b combinationally (same cycle).
    # Reset: none. Power-up state unspecified -> default 0.
    state = 0
    out = []
    for v in vectors:
        a = v.get('a', 0) & 1
        b = v.get('b', 0) & 1
        # R2: combinational output q = a & b (same cycle)
        q = a & b
        # R1: state is the flip-flop value (from previous posedge)
        out.append({'q': q & 1, 'state': state & 1})
        # R1: next state = a & b, captured on posedge clk
        state = a & b
    return out

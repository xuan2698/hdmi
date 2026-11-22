def reference(vectors):
    # Contract implementation.
    # R1: state updates to a AND b on posedge clk (visible next cycle).
    # R2 (candidate interpretation): q = a XOR b combinationally (same cycle).
    # Reset: none. Power-up state unspecified -> use 0 as concrete default.
    # Mid-cycle changes: carried to next row (we just use each row's inputs).
    state = 0
    out = []
    for v in vectors:
        a = v.get('a', 0) & 1
        b = v.get('b', 0) & 1
        # R2: combinational q = a XOR b (candidate interpretation)
        q = a ^ b
        # Outputs reflect current cycle: q combinational, state is current flip-flop value
        out.append({'q': q & 1, 'state': state & 1})
        # R1: posedge update -> next state = a AND b
        state = a & b
    return out

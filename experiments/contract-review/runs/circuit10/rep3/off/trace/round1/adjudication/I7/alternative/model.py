def reference(vectors):
    # Contract implementation.
    # R1: state updates on posedge clk to a XOR b (next_cycle visible).
    # R2: q = state (combinational passthrough, same_cycle).
    # Reset: none. Power-up state unspecified -> use 0 as concrete default.
    state = 0
    out = []
    for row in vectors:
        a = row.get('a', 0)
        b = row.get('b', 0)
        # R2: q reflects current state (combinational)
        q = state
        out.append({'q': q & 1, 'state': state & 1})
        # R1: posedge update to a XOR b
        state = (a ^ b) & 1
    return out

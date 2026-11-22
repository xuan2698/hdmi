def reference(vectors):
    # Contract implementation.
    # R2: q = a XOR b (combinational, same cycle).
    # R1: state <= q on posedge (next cycle visible).
    # Reset: none. Power-up state unspecified -> use 0 as concrete value.
    state = 0
    out = []
    for vec in vectors:
        a = vec.get('a', 0) & 1
        b = vec.get('b', 0) & 1
        # R2: combinational output q
        q = a ^ b
        # R1: state visible this cycle is the value captured at previous posedge
        out.append({'q': q, 'state': state})
        # R1: on posedge, flip-flop captures current q
        state = q
    return out

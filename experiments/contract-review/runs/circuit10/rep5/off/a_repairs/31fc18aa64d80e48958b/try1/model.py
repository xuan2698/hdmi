def reference(vectors):
    # Contract implementation.
    # r1: q is combinational a XOR b, visible next cycle (sampled at posedge).
    # r2: state_next = (a AND b) XOR state, updated at posedge.
    # No reset; power-up state unspecified -> use 0 as concrete initial value.
    state = 0
    out = []
    for v in vectors:
        a = v.get('a', 0) & 1
        b = v.get('b', 0) & 1
        # r1: combinational output q = a XOR b
        q = a ^ b
        # r2: next state = (a AND b) XOR state
        next_state = (a & b) ^ state
        out.append({'q': q, 'state': state})
        state = next_state
    return out

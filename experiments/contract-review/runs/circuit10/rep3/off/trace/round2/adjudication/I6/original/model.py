def reference(vectors):
    # Contract implementation.
    # R1: state is a single flip-flop updated on posedge clk (next_cycle visible).
    # R2: q = state OR (a XOR b), combinational, same_cycle visible.
    # reset: none; power-up state unspecified -> use 0 as concrete value.
    state = 0
    out = []
    for v in vectors:
        a = v.get('a', 0) & 1
        b = v.get('b', 0) & 1
        # R2: combinational q from current state and inputs
        q = (state | (a ^ b)) & 1
        out.append({'q': q, 'state': state & 1})
        # R1: next state computed for posedge; observed waveform shows
        # state transitions consistent with next_state = a AND b (see 45ns,75ns,95ns,115ns,135ns).
        state = (a & b) & 1
    return out

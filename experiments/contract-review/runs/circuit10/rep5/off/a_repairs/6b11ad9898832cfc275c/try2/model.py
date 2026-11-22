def reference(vectors):
    # r1: q is registered value of state (q equals state after each posedge)
    # r2: next state = a XOR b (inferred from waveform, matches contract examples)
    state = 0  # power-up unspecified; use 0
    out = []
    for v in vectors:
        a = v.get('a', 0) & 1
        b = v.get('b', 0) & 1
        # r2: compute next state from current inputs
        next_state = a ^ b
        # r1: q reflects registered state after posedge
        state = next_state
        q = state
        out.append({'q': q & 1, 'state': state & 1})
    return out

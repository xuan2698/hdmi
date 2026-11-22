def reference(vectors):
    # r1: q is the registered value of state (q equals state after each posedge)
    # r2: next state = a XOR b XOR state (inferred from waveform)
    # reset: none; power-up unspecified -> use 0
    state = 0
    out = []
    for v in vectors:
        a = v.get('a', 0) & 1
        b = v.get('b', 0) & 1
        # r1: q reflects current registered state
        q = state & 1
        out.append({'q': q, 'state': state & 1})
        # r2: compute next state at posedge
        state = (a ^ b ^ state) & 1
    return out

def reference(vectors):
    # Contract implementation.
    # r1: q is the registered value of state (q equals state after each posedge).
    # r2: next state = (a XOR b) XOR state, sampled at posedge.
    # reset: none; power-up state unspecified -> use 0 as concrete value.
    state = 0
    q = 0
    out = []
    for v in vectors:
        a = v.get('a', 0) & 1
        b = v.get('b', 0) & 1
        # r1: q reflects registered state (visible after posedge)
        q = state
        # r2: compute next state from current inputs and current state
        nxt = (a ^ b) ^ state
        out.append({'q': q & 1, 'state': state & 1})
        # posedge update
        state = nxt & 1
    return out

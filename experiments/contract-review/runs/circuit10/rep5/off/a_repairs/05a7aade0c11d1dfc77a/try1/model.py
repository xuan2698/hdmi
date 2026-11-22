def reference(vectors):
    # Contract implementation.
    # r1: q is the registered value of state (q equals state after each posedge).
    # r2: next state = (a XOR b) XOR state, sampled on posedge.
    # reset: none; power-up state unspecified -> use 0.
    # mid: optional mid input changes occur AFTER sampling, before the other edge,
    #      and are carried to the start of the next row.
    state = 0
    q = 0
    out = []
    for row in vectors:
        a = row.get('a', 0)
        b = row.get('b', 0)
        # r1: q reflects registered state (visible after posedge)
        q = state
        # r2: compute next state from current inputs and current state
        nxt = (a ^ b) ^ state
        out.append({'q': q & 1, 'state': state & 1})
        # posedge update
        state = nxt & 1
    return out

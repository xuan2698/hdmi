def reference(vectors):
    out = []
    state = 0
    for v in vectors:
        clk = v.get('clk', 0)
        a = v.get('a', 0)
        b = v.get('b', 0)
        # q is combinational: state ^ a (using current state before edge)
        q = state ^ a
        # On posedge, update state
        if clk == 1:
            # state_next = a ? (b ? state : 1) : (b ? 0 : state)
            if a:
                state_next = state if b else 1
            else:
                state_next = 0 if b else state
            state = state_next
        out.append({'q': q & 1, 'state': state & 1})
    return out

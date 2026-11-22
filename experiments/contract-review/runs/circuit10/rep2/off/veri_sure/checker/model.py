def reference(vectors):
    # Sequential circuit: state updates on posedge clk.
    # state_next = (a & ~b) | (state & ~a & ~b) | (state & a & b)
    # q = state XOR a  (combinational, uses current state and inputs)
    # Power-up state is unspecified; use 0 as concrete initial value.
    state = 0
    out = []
    for row in vectors:
        clk = row.get('clk', 0)
        a = row.get('a', 0)
        b = row.get('b', 0)
        # q is combinational from current state and inputs
        q = state ^ a
        # On posedge, update state to next-state function
        if clk == 1:
            state_next = (a & (1 - b)) | (state & (1 - a) & (1 - b)) | (state & a & b)
            state = state_next & 1
        out.append({'state': state & 1, 'q': q & 1})
    return out

def reference(vectors):
    # r1: q is the next-state (combinational) value; state is registered value updated at posedge
    # r2: next state = a XOR b XOR state (waveform-consistent candidate)
    state = 0
    out = []
    for v in vectors:
        a = v['a'] & 1
        b = v['b'] & 1
        # r1: q is combinational next-state
        q = (a ^ b ^ state) & 1
        out.append({'q': q, 'state': state & 1})
        # r2: state updates at posedge to next-state
        state = q
    return out

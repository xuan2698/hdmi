def reference(vectors):
    # Contract:
    # R1: state <= q on posedge (flip-flop captures current q)
    # R2: q = a XOR b (combinational)
    # state is observable; q is combinational output
    # Power-up unspecified: use 0 for state initially
    state = 0
    out = []
    for v in vectors:
        a = v.get('a', 0)
        b = v.get('b', 0)
        # R2: combinational q = a XOR b
        q = (a ^ b) & 1
        # R1: state captures q on posedge (visible next cycle)
        # state output reflects current stored value
        out.append({'q': q, 'state': state & 1})
        # update flip-flop for next cycle
        state = q
    return out

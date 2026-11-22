def reference(vectors):
    # Contract implementation.
    # R2: q = a XOR b (combinational, same cycle)
    # R1: state <= q on posedge (next cycle)
    # Reset: none. Power-up state unspecified; we start state at 0.
    state = 0
    out = []
    for v in vectors:
        a = v.get('a', 0)
        b = v.get('b', 0)
        # R2: combinational output q = a XOR b
        q = a ^ b
        # R1: state captures current q on posedge -> visible next cycle
        # Emit current state (from previous posedge), then update.
        out.append({'q': q, 'state': state})
        state = q
    return out

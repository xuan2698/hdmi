def reference(vectors):
    # Sequential 3-bit state machine.
    # q starts at 4 (power-up value from the trace).
    # On each posedge: if a==1 hold, else q = (q+1) % 7.
    # Output q is the state itself (3 bits).
    q = 4
    out = []
    for row in vectors:
        clk = row.get('clk')
        a = row.get('a')
        # Sample on positive clock edge (after settling).
        if clk == 1:
            if a == 1:
                q = q
            else:
                q = (q + 1) % 7
        out.append({'q': q & 0x7})
    return out

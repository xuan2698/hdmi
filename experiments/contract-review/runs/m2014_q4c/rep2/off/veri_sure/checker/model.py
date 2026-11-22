def reference(vectors):
    # D flip-flop with active-high synchronous reset.
    # On posedge clk: if r==1 -> q<=0 else q<=d.
    # Output q reflects value sampled at previous posedge (latency 1 cycle).
    # Power-up unspecified -> use 0.
    q = 0
    out = []
    for row in vectors:
        # Sample inputs at the posedge (values driven before edge)
        d = row.get('d', 0) & 1
        r = row.get('r', 0) & 1
        # Compute next state from current sampled inputs
        if r == 1:
            nq = 0
        else:
            nq = d
        # Output reflects current registered value (before this edge's update)
        out.append({'q': q & 1})
        # Update register after sampling
        q = nq
    return out

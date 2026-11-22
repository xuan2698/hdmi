def reference(vectors):
    # Rule q_posedge_update: candidate interpretation applied -> negedge-triggered D flip-flop.
    # q holds at posedge; updates at negedge using d and r (r active high synchronous reset).
    # Power-up is unspecified; we use a concrete initial value of 0.
    q = 0
    out = []
    for row in vectors:
        # q_posedge_update: posedge does not update q for a negedge-triggered FF.
        # Output is sampled after the posedge has settled, before the negedge.
        out.append({"q": q & 1})
        
        # Inputs driven before the sampled posedge.
        d = row.get("d", 0)
        r = row.get("r", 0)
        
        # mid changes occur after the posedge and before the negedge.
        mid = row.get("mid", {})
        d_neg = mid.get("d", d)
        r_neg = mid.get("r", r)
        
        # q_posedge_update: negedge-triggered update.
        # If r==1 then q becomes 0; otherwise q becomes d.
        if r_neg == 1:
            q = 0
        else:
            q = d_neg & 1
    return out

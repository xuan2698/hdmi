def reference(vectors):
    # State: count (0..9), initial unspecified -> use 0 as concrete power-up value.
    # R1: reset==1 at posedge -> q=0 (sync, priority 1)
    # R2: reset==0 && q==9 at posedge -> q=0 (wrap, priority 2)
    # R3: reset==0 && q!=9 at posedge -> q=q+1 (priority 3)
    count = 0
    out = []
    for row in vectors:
        reset = row.get("reset", 0)
        # Sample at posedge: compute next state from current state and inputs
        if reset == 1:
            # R1
            count = 0
        elif count == 9:
            # R2
            count = 0
        else:
            # R3
            count = count + 1
        out.append({"q": count & 0xF})
    return out

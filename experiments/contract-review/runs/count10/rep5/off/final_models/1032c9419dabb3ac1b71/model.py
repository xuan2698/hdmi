def reference(vectors):
    # Contract implementation.
    # State: COUNT (4-bit q), advances on posedge clk when reset==0.
    # R1: reset==1 on posedge -> q=0 (sync, priority 1)
    # R2: reset==0 && q<9 on posedge -> q=q+1 (priority 2)
    # R3: reset==0 && q==9 on posedge -> q=0 (priority 3)
    # Mid changes occur AFTER sampling, carried to next row.
    q = 0  # power-up unspecified; use 0 as concrete value
    out = []
    for row in vectors:
        # Apply any mid changes carried from previous row are already in row
        reset = row.get('reset', 0)
        # Sample at posedge: compute next state based on current inputs and state
        # R1
        if reset == 1:
            q = 0
        # R2
        elif q < 9:
            q = q + 1
        # R3
        else:  # q == 9
            q = 0
        out.append({'q': q & 0xF})
    return out

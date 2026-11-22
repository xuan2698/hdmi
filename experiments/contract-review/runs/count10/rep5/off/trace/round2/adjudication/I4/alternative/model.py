def reference(vectors):
    # Contract implementation.
    # State: COUNT (4-bit q). Initial q = 0 at time zero (candidate interpretation for global).
    # R1: reset==1 on posedge -> q=0 (sync, active high), priority 1.
    # R2: reset==0 && q<9 on posedge -> q=q+1, priority 2.
    # R3: reset==0 && q==9 on posedge -> q=0, priority 3.
    # Mid changes occur AFTER sampling, before other edge, carried to next row.

    q = 0  # initial state at time zero
    out = []
    for row in vectors:
        reset = row.get('reset', 0)
        # Sample at posedge: compute next state based on current q and reset
        # R1
        if reset == 1:
            q_next = 0
        # R2
        elif q < 9:
            q_next = q + 1
        # R3
        else:  # q == 9
            q_next = 0
        # Output visible same cycle (after posedge settles)
        out.append({'q': q_next & 0xF})
        # Mid changes: apply after sampling, carried to next row.
        # (No mid inputs defined beyond reset which is a row input; nothing to do.)
        q = q_next
    return out

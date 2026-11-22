def reference(vectors):
    # Sequential circuit inferred from waveform:
    # State: a_reg (1 bit), q_reg (3 bits)
    # On posedge clk:
    #   a_reg <= a
    #   if a_reg == 1: q_reg <= 4
    #   else: q_reg <= (q_reg + 1) mod 7
    # Output q = q_reg
    # Initial state: a_reg = 1, q_reg = 0 (q unspecified at time 0)
    a_reg = 1
    q_reg = 0
    results = []
    for row in vectors:
        # Each row provides values driven before the sampled posedge.
        # We sample after the posedge has settled.
        a = row['a']
        # Compute next state based on current state and input a
        # (a_reg is the value from the previous cycle)
        if a_reg == 1:
            next_q = 4
        else:
            if q_reg == 6:
                next_q = 0
            else:
                next_q = q_reg + 1
        next_a_reg = a
        # Update state (posedge occurs)
        a_reg = next_a_reg
        q_reg = next_q
        # Output after posedge
        results.append({'q': q_reg})
    return results

def reference(vectors):
    # State: q_reg holds the 8-bit flip-flop storage, initial value 0.
    q_reg = 0
    results = []
    for row in vectors:
        d = row['d']
        reset = row['reset']
        # R1_sync_reset: active high synchronous reset sets output to zero on posedge.
        # R2_d_capture: when reset == 0, capture d on posedge.
        # Both rules are evaluated at the posedge; reset has priority 1.
        if reset == 1:
            q_reg = 0  # R1_sync_reset
        else:
            q_reg = d & 0xFF  # R2_d_capture
        results.append({'q': q_reg})
    return results

def reference(vectors):
    # Contract:
    # - Synchronous active-high reset clears the sticky output at the posedge.
    # - out is sticky: once a bit captures a 1->0 transition, it stays 1 until reset.
    # - Falling edge detected per bit as prev_in & ~in, using edge-sampled values.
    # - prev_in updates unconditionally every cycle (even during reset) so a real
    #   1->0 transition spanning a reset boundary is still detected next cycle.
    # - Mid-cycle input changes occur after sampling and only affect the next row.
    # - Power-up state: out = 0, prev_in = 0.
    out = 0
    prev_in = 0
    results = []
    for row in vectors:
        reset = row.get('reset', 0) & 1
        inp = row.get('in', 0) & 0xFFFFFFFF
        # Compute next state from edge-sampled values.
        if reset:
            next_out = 0
        else:
            next_out = (out | (prev_in & (~inp & 0xFFFFFFFF))) & 0xFFFFFFFF
        next_prev = inp
        out = next_out
        prev_in = next_prev
        results.append({'out': out})
    return results

def reference(vectors):
    # Contract implementation.
    # R1: state <= q, flip-flop captures current q. Candidate interpretation:
    #     state updates on posedge instead of negedge.
    # R2: q = state XOR a XOR b (combinational, same cycle).
    #
    # Timing model: each row's inputs are driven before the sampled posedge.
    # We sample at the posedge: compute q from current state and inputs (R2),
    # then update state to that q for the next cycle (R1, posedge variant).
    # Mid changes occur after sampling and are carried to the next row, so
    # they don't affect this row's outputs.

    state = 0  # power-up unspecified; concrete default
    results = []
    for vec in vectors:
        a = vec.get('a', 0) & 1
        b = vec.get('b', 0) & 1
        # R2: combinational output using state
        q = (state ^ a ^ b) & 1
        results.append({'q': q, 'state': state})
        # R1: state captures q on posedge (candidate interpretation)
        state = q
    return results

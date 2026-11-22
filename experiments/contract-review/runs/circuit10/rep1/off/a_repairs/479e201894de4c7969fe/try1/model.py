def reference(vectors):
    # Contract implementation.
    # R1: state <= q on negedge (flip-flop captures current q). Visible next cycle.
    # R2: q = state XOR a XOR b (combinational, same cycle).
    # Reset: none. Power-up unspecified -> use 0 for concrete values.
    # Mid changes: applied after sampling, carried to next row.

    state = 0  # power-up unspecified, concrete default
    out = []

    for vec in vectors:
        a = vec.get('a', 0) & 1
        b = vec.get('b', 0) & 1

        # R2: combinational q from current state and inputs
        q = (state ^ a ^ b) & 1

        # Outputs for this row (sampled after posedge settled)
        out.append({'q': q, 'state': state})

        # R1: negedge update: state <= q (captures current q)
        state = q

    return out

def reference(vectors):
    # Contract implementation.
    # R1: state <= q on posedge (visible next cycle)
    # R2: q = state XOR a XOR b (combinational, same cycle)
    # Reset: none. Power-up state unspecified -> use 0.
    # Mid changes: inputs may change after sampling; carried to next row.
    # Sampling: after posedge settles. We model: at each row, compute q from
    # current state and inputs (R2), then on posedge capture q into state (R1).
    # Since state update is visible next cycle, we output current state and q,
    # then update state = q for the next row.

    state = 0  # power-up unspecified; concrete default
    out = []
    for row in vectors:
        a = int(row.get('a', 0)) & 1
        b = int(row.get('b', 0)) & 1
        # R2: combinational output using current state
        q = (state ^ a ^ b) & 1
        # Outputs for this row: state (current) and q
        out.append({'q': q, 'state': state & 1})
        # R1: posedge captures q into state for next cycle
        state = q & 1
    return out

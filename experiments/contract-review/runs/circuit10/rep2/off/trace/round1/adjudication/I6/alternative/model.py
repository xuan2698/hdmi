def reference(vectors):
    # Contract implementation.
    # R1: state is a single flip-flop updated on posedge clk to next_state = a XOR b.
    # R2 (candidate interpretation): q = a AND b, combinational, same cycle.
    # Reset: none. Power-up state unspecified -> use 0 as concrete default.
    # Mid-cycle input changes occur after sampling and carry to next row.

    state = 0  # power-up unspecified; concrete default
    out = []

    for row in vectors:
        a = row.get('a', 0)
        b = row.get('b', 0)

        # R2: combinational output q = a AND b (candidate interpretation)
        q = a & b

        # Outputs visible this cycle: q (combinational) and state (current flip-flop value)
        out.append({'q': q & 1, 'state': state & 1})

        # R1: posedge clk updates state to a XOR b for next cycle
        state = (a ^ b) & 1

    return out

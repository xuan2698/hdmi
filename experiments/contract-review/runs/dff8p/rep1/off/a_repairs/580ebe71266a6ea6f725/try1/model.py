def reference(vectors):
    # State: q_state holds the 8-bit value stored in the D flip-flops.
    # Updated on the negative edge of clk.
    # R1: reset == 1 -> q = 0x34 (52) on negedge, same cycle visible.
    # R2: reset == 0 -> q = d on negedge, same cycle visible.
    # Mid changes occur AFTER sampling, before the other edge, carried to next row.
    q_state = 0x34  # power-up unspecified; use reset value as concrete default
    out = []
    for row in vectors:
        d = row.get('d', 0) & 0xFF
        reset = row.get('reset', 0) & 0x1
        # negedge sampling: compute next state
        if reset == 1:  # R1
            q_state = 0x34
        else:  # R2
            q_state = d
        out.append({'q': q_state & 0xFF})
        # mid changes would be applied here (after sampling) if present;
        # they are carried to the start of the next row via row inputs.
    return out

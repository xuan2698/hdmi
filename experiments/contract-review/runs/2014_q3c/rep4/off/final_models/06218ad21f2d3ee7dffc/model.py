def reference(vectors):
    # R_Y0: Y0 = next-state bit 0 per state-assigned table (combinational, same cycle)
    # R_z: z = 1 when present state y is 011 or 100, else 0 (Moore, combinational)
    # Undefined states 101,110,111 -> Y0=0, z=0 (per chosen interpretation)
    # state_register: y updated on posedge clk from next-state function; no reset.
    # mid: optional mid input changes occur AFTER sampling, before other edge,
    #      carried to start of next row. We model y as the present-state register.
    # Protocol seed 20261123: deterministic; we just process rows in order.

    # Next-state function Y[2:0] per table (x=0, x=1)
    # y=000 -> 000, 001
    # y=001 -> 001, 100
    # y=010 -> 010, 001
    # y=011 -> 001, 010
    # y=100 -> 011, 100
    # y=101,110,111 -> undefined; treat as don't-care -> keep? We'll use Y=000 (safe) but
    #   since Y0 for undefined is 0 per interpretation, and next state unspecified,
    #   we choose Y=000 for determinism (only Y0 matters for output; z depends on y).
    next_state = {
        0b000: (0b000, 0b001),
        0b001: (0b001, 0b100),
        0b010: (0b010, 0b001),
        0b011: (0b001, 0b010),
        0b100: (0b011, 0b100),
        0b101: (0b000, 0b000),
        0b110: (0b000, 0b000),
        0b111: (0b000, 0b000),
    }

    # Present-state register y (3-bit). Power-up unspecified; we start at 0.
    y = 0

    results = []
    for row in vectors:
        x = row.get('x', 0) & 1
        # If row provides y explicitly, use it as present state (driven before edge).
        if 'y' in row:
            y = row['y'] & 0b111

        # Combinational outputs from present state y and input x (same cycle)
        # R_Y0
        Y = next_state[y][x]
        Y0 = Y & 1
        # R_z
        z = 1 if (y == 0b011 or y == 0b100) else 0

        results.append({'Y0': Y0, 'z': z})

        # state_register update on posedge clk: y <- Y
        y = Y

    return results

def reference(vectors):
    # Contract implementation.
    # R_Y0: Y0 is bit 2 (MSB) of next-state Y[2:0] per state-assigned table.
    #   y=000 -> x=0: Y=000 -> Y0=0 ; x=1: Y=001 -> Y0=0
    #   y=001 -> x=0: Y=001 -> Y0=0 ; x=1: Y=100 -> Y0=1
    #   y=010 -> x=0: Y=010 -> Y0=0 ; x=1: Y=001 -> Y0=0
    #   y=011 -> x=0: Y=001 -> Y0=0 ; x=1: Y=010 -> Y0=0
    #   y=100 -> x=0: Y=011 -> Y0=0 ; x=1: Y=100 -> Y0=1
    #   y=101,110,111 unspecified -> implementation-defined (choose 0)
    # R_z: z=1 when y in {011,100}, else 0; unspecified states -> 0.
    # state_register: y updated on posedge clk from next-state; no reset.
    # mid: mid input changes occur AFTER sampling, before other edge,
    #      carried to start of next row. We model y as persistent register.

    # Next-state table: Y[2:0] for (y, x)
    # Represent as dict: (y, x) -> Y (3-bit)
    next_state = {
        (0, 0): 0b000, (0, 1): 0b001,
        (1, 0): 0b001, (1, 1): 0b100,
        (2, 0): 0b010, (2, 1): 0b001,
        (3, 0): 0b001, (3, 1): 0b010,
        (4, 0): 0b011, (4, 1): 0b100,
    }

    def get_next(y, x):
        # R_Y0: unspecified states 101,110,111 -> implementation-defined 0
        return next_state.get((y & 0x7, x & 0x1), 0b000)

    def compute_Y0(y, x):
        # R_Y0: Y0 = bit 2 (MSB) of Y[2:0]
        Y = get_next(y, x)
        return (Y >> 2) & 1

    def compute_z(y):
        # R_z: z=1 for y=011 or y=100
        return 1 if (y & 0x7) in (0b011, 0b100) else 0

    results = []
    # state_register: present-state y, updated on posedge clk.
    # No reset specified; power-up unspecified -> start at 0 (concrete).
    y = 0

    for vec in vectors:
        x = vec.get('x', 0) & 0x1
        # If vector provides y explicitly, that's the present state for this row.
        if 'y' in vec:
            y = vec['y'] & 0x7

        # Combinational outputs visible same cycle (R_Y0, R_z)
        Y0 = compute_Y0(y, x)
        z = compute_z(y)

        results.append({'Y0': Y0, 'z': z})

        # state_register update on posedge clk: y <- Y[2:0]
        # mid changes occur AFTER sampling, carried to next row.
        y = get_next(y, x)

    return results

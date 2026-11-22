def reference(vectors):
    # R_Y0: Y0 = next-state bit 0 of Y[2:0] per state-assigned table
    # R_z: z = 1 when present state y[2:0] is 011 or 100, else 0
    # state_register: 3-bit present-state register y[2:0] updated on posedge clk
    #   from next-state function Y[2:0]; no reset.
    # mid: optional mid input changes occur AFTER sampling, before the other
    #   edge, and are carried to the start of the next row.

    # Next-state table: next_state[y][x] = (Y2, Y1, Y0)
    next_state = {
        0: {0: (0, 0, 0), 1: (0, 0, 1)},
        1: {0: (0, 0, 1), 1: (1, 0, 0)},
        2: {0: (0, 1, 0), 1: (0, 0, 1)},
        3: {0: (0, 0, 1), 1: (0, 1, 0)},
        4: {0: (0, 1, 1), 1: (1, 0, 0)},
    }

    # Moore output z from present state
    def z_of(y):
        return 1 if y in (3, 4) else 0

    results = []
    # Present-state register; power-up unspecified -> use 0 as concrete value.
    y = 0

    for vec in vectors:
        x = vec["x"]
        # Present state y is the register value at sampling time.
        # R_z: combinational Moore output from present state.
        z = z_of(y)
        # R_Y0: combinational next-state bit 0 from present state and x.
        Y0 = next_state[y][x][2]
        results.append({"Y0": Y0, "z": z})
        # state_register: update on posedge clk from next-state function.
        y = (next_state[y][x][0] << 2) | (next_state[y][x][1] << 1) | next_state[y][x][2]

    return results

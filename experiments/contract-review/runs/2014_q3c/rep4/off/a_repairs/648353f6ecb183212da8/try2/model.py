def reference(vectors):
    # R_Y0: Y0 = next-state bit 0 of Y[2:0] per state-assigned table
    # R_z: z = 1 when present state y[2:0] is 011 or 100, else 0
    # state_register: 3-bit present-state register y[2:0] updated on posedge clk
    #   from next-state function Y[2:0]; no reset.
    # mid: optional mid input changes occur AFTER sampling, before the other
    #   edge, and are carried to the start of the next row.

    # Next-state table: next_state[y][x] -> Y[2:0]
    next_state = {
        0: {0: 0, 1: 1},  # 000 -> x=0:000, x=1:001
        1: {0: 1, 1: 4},  # 001 -> x=0:001, x=1:100
        2: {0: 2, 1: 1},  # 010 -> x=0:010, x=1:001
        3: {0: 1, 1: 2},  # 011 -> x=0:001, x=1:010
        4: {0: 3, 1: 4},  # 100 -> x=0:011, x=1:100
    }

    # Present-state register, power-up unspecified -> concrete 0
    y = 0

    results = []
    for row in vectors:
        x = row["x"] & 1
        # Present state y is the register value at sampling time.
        # R_Y0: combinational next-state bit 0
        Y = next_state[y][x]
        Y0 = Y & 1
        # R_z: Moore output from present state
        z = 1 if (y == 3 or y == 4) else 0
        results.append({"Y0": Y0, "z": z})
        # state_register: update on posedge clk from next-state function
        y = Y
        # mid changes are carried to start of next row (no effect here since
        # inputs are re-read per row)
    return results

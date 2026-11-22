def reference(vectors):
    # Contract:
    # - Inputs: clk, x (1 bit), y (3 bits)
    # - Outputs: Y0 (1 bit), z (1 bit)
    # - Outputs are combinational functions of current y and x, sampled after posedge settles.
    # - Each row's values are driven before the sampled edge.
    # - Optional mid input changes occur AFTER sampling, before the other edge,
    #   and are carried to the start of the next row.
    # - Return a dict per row with every output as a concrete unsigned integer.

    # Next-state table: y -> (Y when x=0, Y when x=1)
    next_state = {
        0b000: (0b000, 0b001),
        0b001: (0b001, 0b100),
        0b010: (0b010, 0b001),
        0b011: (0b001, 0b010),
        0b100: (0b011, 0b100),
    }

    # Moore output z: 0 for y in {000,001,010}; 1 for y in {011,100}
    z_table = {
        0b000: 0,
        0b001: 0,
        0b010: 0,
        0b011: 1,
        0b100: 1,
    }

    results = []
    for row in vectors:
        # Extract current inputs for this row
        x = row.get("x", 0) & 0x1
        y = row.get("y", 0) & 0x7

        # Compute next state Y based on current y and x
        y0_next, y1_next = next_state.get(y, (0, 0))
        Y = y0_next if x == 0 else y1_next

        # Y0 is bit 0 of next state Y
        Y0 = Y & 0x1

        # z is Moore output for present state y
        z = z_table.get(y, 0)

        results.append({"Y0": Y0, "z": z})

    return results

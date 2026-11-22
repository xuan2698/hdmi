def reference(vectors):
    # Contract:
    # - Inputs: clk, x, y[2:0]; outputs: Y0, z (both combinational).
    # - Y0 = bit 0 of next state Y[2:0] given present state y and input x.
    # - z = 1 iff y in {011, 100}, else 0.
    # - Each row: drive values before sampled posedge; sample after settling.
    # - Mid changes occur AFTER sampling, before next edge, carried to next row.
    # - Return dict per row with all outputs as unsigned ints within bit width.
    results = []
    for row in vectors:
        y = row.get('y', 0) & 0x7
        x = row.get('x', 0) & 0x1

        # Next state table
        if y == 0b000:
            nxt = 0b001 if x == 1 else 0b000
        elif y == 0b001:
            nxt = 0b100 if x == 1 else 0b001
        elif y == 0b010:
            nxt = 0b001 if x == 1 else 0b010
        elif y == 0b011:
            nxt = 0b010 if x == 1 else 0b001
        elif y == 0b100:
            nxt = 0b100 if x == 1 else 0b011
        else:
            nxt = 0b000

        Y0 = nxt & 0x1
        z = 1 if (y == 0b011 or y == 0b100) else 0

        results.append({'Y0': Y0, 'z': z})
    return results

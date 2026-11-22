def reference(vectors):
    # State-assigned table:
    # y[2:0] | Y[2:0] x=0 | Y[2:0] x=1 | z
    # 000    | 000        | 001        | 0
    # 001    | 001        | 100        | 0
    # 010    | 010        | 001        | 0
    # 011    | 001        | 010        | 1
    # 100    | 011        | 100        | 1
    #
    # We only need Y[0] (LSB of next state) and z.
    # Y0 = LSB of next state.
    # z depends only on present state y.
    #
    # Table for Y0:
    # y=000: x=0 -> Y=000 -> Y0=0 ; x=1 -> Y=001 -> Y0=1
    # y=001: x=0 -> Y=001 -> Y0=1 ; x=1 -> Y=100 -> Y0=0
    # y=010: x=0 -> Y=010 -> Y0=0 ; x=1 -> Y=001 -> Y0=1
    # y=011: x=0 -> Y=001 -> Y0=1 ; x=1 -> Y=010 -> Y0=0
    # y=100: x=0 -> Y=011 -> Y0=1 ; x=1 -> Y=100 -> Y0=0
    #
    # z table:
    # y=000:0, 001:0, 010:0, 011:1, 100:1
    #
    # Unlisted states: unspecified -> we still must return concrete ints.
    # We'll default to 0 for unspecified (won't be checked).
    #
    # Timing: latch y and x at posedge; mid changes after sampling belong to next row.
    # The vectors presumably provide per-row sampled values. We compute from
    # the sampled y and x for each row.

    y0_table = {
        0b000: {0: 0, 1: 1},
        0b001: {0: 1, 1: 0},
        0b010: {0: 0, 1: 1},
        0b011: {0: 1, 1: 0},
        0b100: {0: 1, 1: 0},
    }
    z_table = {
        0b000: 0,
        0b001: 0,
        0b010: 0,
        0b011: 1,
        0b100: 1,
    }

    results = []
    for row in vectors:
        y = row.get('y', 0) & 0x7
        x = row.get('x', 0) & 0x1
        if y in y0_table:
            Y0 = y0_table[y][x]
            z = z_table[y]
        else:
            Y0 = 0
            z = 0
        results.append({'Y0': Y0, 'z': z})
    return results

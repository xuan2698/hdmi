def reference(vectors):
    # Contract implementation.
    # R_Y0: Y0 = next-state bit 0 (LSB) of Y[2:0] per state-assigned table.
    #   y=000 -> x=0:0, x=1:1
    #   y=001 -> x=0:1, x=1:0
    #   y=010 -> x=0:0, x=1:1
    #   y=011 -> x=0:1, x=1:0
    #   y=100 -> x=0:1, x=1:0
    #   y=101,110,111 unspecified -> implementation-defined (choose 0)
    # R_z: z = 1 when y in {011, 100}, else 0 (Moore output).
    #   y=101,110,111 unspecified -> implementation-defined (choose 0)
    # state_register: y updated on posedge clk from next-state Y[2:0].
    #   We track y across rows; each row's y is the present state at sampling.
    #   After sampling, y becomes the next state Y[2:0] computed from (x, y).
    #   Mid input changes occur after sampling, before other edge, carried to next row.
    #   Since only Y0 is exposed, we must reconstruct full Y[2:0] to update y.
    #   Full next-state table (from spec):
    #     y=000: x=0->000, x=1->001
    #     y=001: x=0->001, x=1->100
    #     y=010: x=0->010, x=1->001
    #     y=011: x=0->001, x=1->010
    #     y=100: x=0->011, x=1->100
    #     y=101,110,111: unspecified -> implementation-defined (hold y)

    # next-state full table: key (y, x) -> Y[2:0]
    next_state = {
        (0, 0): 0, (0, 1): 1,
        (1, 0): 1, (1, 1): 4,
        (2, 0): 2, (2, 1): 1,
        (3, 0): 1, (3, 1): 2,
        (4, 0): 3, (4, 1): 4,
    }

    # R_Y0: Y0 = LSB of next-state Y[2:0]
    def compute_Y0(y, x):
        key = (y & 7, x & 1)
        if key in next_state:
            return next_state[key] & 1
        return 0  # unspecified -> implementation-defined

    # R_z: Moore output
    def compute_z(y):
        yv = y & 7
        if yv in (3, 4):
            return 1
        return 0  # includes unspecified 5,6,7 -> implementation-defined 0

    results = []
    y = 0  # present state register, initial value unspecified; choose 0

    for vec in vectors:
        x = vec.get('x', 0) & 1
        # If vector provides y explicitly, use it as present state (per example vectors)
        if 'y' in vec:
            y = vec['y'] & 7

        # Sample combinational outputs at this row (same_cycle visibility)
        Y0 = compute_Y0(y, x)
        z = compute_z(y)
        results.append({'Y0': Y0, 'z': z})

        # state_register update on posedge clk: y <- next state Y[2:0]
        key = (y & 7, x & 1)
        if key in next_state:
            y = next_state[key]
        # else unspecified: hold y (implementation-defined)

    return results

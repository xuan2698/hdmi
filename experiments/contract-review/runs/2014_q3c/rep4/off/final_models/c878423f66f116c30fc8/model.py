def reference(vectors):
    # State register: 3-bit present-state y[2:0], updated on posedge clk.
    # No reset; power-up unspecified -> we start from 0 (concrete value required).
    state = 0  # present state y[2:0]

    # R_Y0: Y0 = next-state bit 0 (LSB) of Y[2:0] per state-assigned table.
    # Table (y -> x=0 next, x=1 next):
    #   000 -> 000, 001
    #   001 -> 001, 100
    #   010 -> 010, 001
    #   011 -> 001, 010
    #   100 -> 011, 100
    # Unspecified states 101,110,111 -> implementation-defined; use 000.
    next_table = {
        0b000: (0b000, 0b001),
        0b001: (0b001, 0b100),
        0b010: (0b010, 0b001),
        0b011: (0b001, 0b010),
        0b100: (0b011, 0b100),
    }

    def next_state(y, x):
        # R_Y0: next-state function; unspecified states default to 000.
        if y in next_table:
            return next_table[y][x]
        return 0b000

    def compute_Y0(y, x):
        # R_Y0: Y0 is bit 0 (LSB) of next-state Y[2:0].
        return next_state(y, x) & 0b001

    def compute_z(y):
        # R_z: Moore output z = 1 iff present state is 011 or 100.
        return 1 if y in (0b011, 0b100) else 0

    results = []
    for row in vectors:
        x = row.get("x", 0) & 0b1
        y = row.get("y", state) & 0b111

        # Combinational outputs visible same cycle, based on present state y.
        Y0 = compute_Y0(y, x)
        z = compute_z(y)

        results.append({"Y0": Y0 & 0b1, "z": z & 0b1})

        # posedge clk: state register updates from next-state function.
        # Mid input changes occur AFTER sampling, before other edge,
        # carried to start of next row -> we simply update state here.
        state = next_state(y, x)

    return results

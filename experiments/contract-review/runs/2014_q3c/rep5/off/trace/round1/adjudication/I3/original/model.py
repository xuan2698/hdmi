def reference(vectors):
    # R_Y0: Y0 = next-state bit 0 as function of y and x per state-assigned table
    # R_z: z = 1 for present states 011 and 100, else 0
    # present_state updates on posedge clk to next state Y[2:0]
    # mid input changes occur AFTER sampling, before the other edge, carried to start of next row
    # state-assigned table:
    # y=000: x=0 -> Y=000, x=1 -> Y=001
    # y=001: x=0 -> Y=001, x=1 -> Y=100
    # y=010: x=0 -> Y=010, x=1 -> Y=001
    # y=011: x=0 -> Y=001, x=1 -> Y=010
    # y=100: x=0 -> Y=011, x=1 -> Y=100

    # next state function
    def next_state(y, x):
        if y == 0b000:
            return 0b000 if x == 0 else 0b001
        elif y == 0b001:
            return 0b001 if x == 0 else 0b100
        elif y == 0b010:
            return 0b010 if x == 0 else 0b001
        elif y == 0b011:
            return 0b001 if x == 0 else 0b010
        elif y == 0b100:
            return 0b011 if x == 0 else 0b100
        else:
            return 0b000

    def z_out(y):
        return 1 if (y == 0b011 or y == 0b100) else 0

    results = []
    state = 0  # present_state, power-up unspecified but concrete
    for vec in vectors:
        x = vec['x']
        y = vec['y']
        # combinational outputs based on present state y
        Y0 = next_state(y, x) & 1
        z = z_out(y)
        results.append({'Y0': Y0, 'z': z})
        # posedge clk: present_state updates to next state
        state = next_state(y, x)
    return results

def reference(vectors):
    # State table: present state -> (next state for x=0, next state for x=1, z)
    # R_Y0, R_z: combinational outputs from present state y and input x
    table = {
        0b000: (0b000, 0b001, 0),
        0b001: (0b001, 0b100, 0),
        0b010: (0b010, 0b001, 0),
        0b011: (0b001, 0b010, 1),
        0b100: (0b011, 0b100, 1),
    }
    # R_z: unspecified states 101,110,111 -> z=0 (per chosen interpretation)
    # R_Y0: unspecified states -> Y0 don't-care; use 0 as concrete value
    results = []
    for vec in vectors:
        x = vec["x"] & 1
        y = vec["y"] & 0b111
        if y in table:
            nxt0, nxt1, z = table[y]
            nxt = nxt1 if x else nxt0
            Y0 = nxt & 1
        else:
            # R_Y0: unspecified state -> Y0 don't-care, concrete 0
            # R_z: unspecified state -> z=0
            Y0 = 0
            z = 0
        results.append({"Y0": Y0 & 1, "z": z & 1})
    return results

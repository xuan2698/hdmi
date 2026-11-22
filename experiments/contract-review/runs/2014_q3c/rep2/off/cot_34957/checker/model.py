def reference(vectors):
    # State-assigned table:
    # present y[2:0] -> (next if x=0, next if x=1, z)
    table = {
        0b000: (0b000, 0b001, 0),
        0b001: (0b001, 0b100, 0),
        0b010: (0b010, 0b001, 0),
        0b011: (0b001, 0b010, 1),
        0b100: (0b011, 0b100, 1),
    }

    results = []
    for vec in vectors:
        # Each vector provides sampled y and x at the active edge.
        y = vec.get("y", 0) & 0b111
        x = vec.get("x", 0) & 0b1

        if y in table:
            n0, n1, z = table[y]
        else:
            # Unspecified present state: no defined behavior; use safe defaults.
            n0, n1, z = 0, 0, 0

        nxt = n1 if x else n0
        Y0 = nxt & 0b1  # Y[0] is the LSB of the next state

        results.append({
            "Y0": Y0 & 0b1,
            "z": z & 0b1,
        })

    return results

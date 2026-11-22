def reference(vectors):
    q = 0          # power-up unspecified: use concrete initial value
    prev_a = 0     # reset none: concrete initial previous a
    out = []

    for row in vectors:
        a = row.get("a", 0)
        if a is None:
            a = 0
        else:
            a = int(a) & 1

        # R1_a_high_load4: a == 1 at posedge => q <= 4 (priority 1)
        if a == 1:
            q = 4
        # R2_first_low_hold: a == 0 && prev_a == 1 => q <= q
        elif prev_a == 1:
            q = q
        # R3_count_low: a == 0 && prev_a == 0 => q <= (q + 1) mod 7
        else:
            q = (q + 1) % 7

        prev_a = a
        out.append({"q": q})

    return out

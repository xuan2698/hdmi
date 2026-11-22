def reference(vectors):
    # Initial state: q=4 (initial load/init to 4), prev_a=1 (first low holds per R2 interpretation)
    q = 4
    prev_a = 1
    out = []
    for vec in vectors:
        a = vec['a']
        # R1_a_high_load4: a=1 only holds current q after initial load/init to 4; no reload on later high.
        if a == 1:
            q = q
        # R2_first_low_hold: a=0 and prev_a=1 => hold.
        elif prev_a == 1:
            q = q
        # R3_count_low: a=0 and prev_a=0 => increment modulo 7.
        else:
            q = (q + 1) % 7
        prev_a = a
        out.append({'q': q})
    return out

def reference(vectors):
    # Initial concrete state (power-up unspecified; use 0 for determinism).
    q = 0
    c = 0
    out = []

    for vec in vectors:
        a = vec.get('a', 0)

        if a == 1:
            # R1_a_high_load4: a == 1 at posedge loads/holds q at 4.
            # Candidate interpretation for R2: a == 1 also loads internal c = 4.
            q_next = 4
            c_next = 4
        else:
            # R2_first_low_hold override: q is registered c (one-cycle delayed).
            # This produces the first-low hold after a high sample.
            q_next = c

            # R3_count_low: internal c increments modulo 7 on a == 0 posedge.
            c_next = (c + 1) % 7

        q = q_next
        c = c_next

        # q is a 3-bit unsigned output.
        out.append({'q': q & 0x7})

    return out

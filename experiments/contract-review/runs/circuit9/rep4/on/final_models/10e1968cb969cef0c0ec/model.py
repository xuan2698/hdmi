def reference(vectors):
    # Named state: q = 3-bit modulo-7 up-counter value
    # Named state: prev_a = value of a sampled at previous posedge
    q = 0       # power-up concrete default (unspecified -> 0)
    prev_a = 0  # power-up concrete default (unspecified -> 0)
    outputs = []

    for v in vectors:
        a = v['a'] & 1  # input width is 1

        # Explicit priority transition for posedge update
        if a == 1:
            # R1_a_high_load4: a == 1 at posedge => q <= 4
            q = 4
        else:  # a == 0
            if prev_a == 1:
                # R2_first_low_hold: a == 0 && prev_a == 1 => q <= q
                pass
            else:  # prev_a == 0
                # R3_count_low: a == 0 && prev_a == 0 => q <= (q + 1) mod 7
                q = (q + 1) % 7

        # prev_a updates to current a on each posedge
        prev_a = a

        # same_cycle visibility: output q after the posedge update
        outputs.append({'q': q})

    return outputs

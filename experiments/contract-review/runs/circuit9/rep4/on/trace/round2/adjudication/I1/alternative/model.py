def reference(vectors):
    q = 0
    prev_a = 0
    first = 1
    result = []
    for vec in vectors:
        a = vec["a"]
        if first:
            # R1_a_high_load4: first posedge initializes q=4; later a=1 holds current q.
            q = 4
            first = 0
        else:
            if a == 1:
                # R1_a_high_load4: later a=1 holds current q instead of reloading 4.
                q = q
            else:
                if prev_a == 1:
                    # R2_first_low_hold: first low sample after a high holds q.
                    q = q
                else:
                    # R3_count_low: consecutive low samples increment modulo 7.
                    q = q + 1
                    if q == 7:
                        q = 0
        prev_a = a
        result.append({"q": q})
    return result

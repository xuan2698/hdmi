def reference(vectors):
    # States: S0 (no prefix), S1 (seen "1"), S2 (seen "11"), S3 (seen "110"), FOUND
    # start_shifting is 0 until FOUND, then 1 forever until reset.
    state = 0  # 0=S0, 1=S1, 2=S2, 3=S3, 4=FOUND
    out = []
    for row in vectors:
        reset = row['reset'] & 1
        data = row['data'] & 1
        # synchronous reset takes priority
        if reset:
            state = 0
        else:
            if state == 0:
                state = 1 if data == 1 else 0
            elif state == 1:
                state = 2 if data == 1 else 0
            elif state == 2:
                state = 3 if data == 0 else 2
            elif state == 3:
                state = 4 if data == 1 else 0
            elif state == 4:
                state = 4
        start_shifting = 1 if state == 4 else 0
        out.append({'start_shifting': start_shifting})
    return out

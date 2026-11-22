def reference(vectors):
    out_reg = 0
    prev_in = 0
    results = []
    for row in vectors:
        reset = row['reset'] & 1
        inp = row['in'] & 0xFFFFFFFF
        if reset:
            out_reg = 0
        else:
            out_reg = out_reg | (prev_in & (~inp & 0xFFFFFFFF))
            prev_in = inp
        results.append({'out': out_reg & 0xFFFFFFFF})
    return results

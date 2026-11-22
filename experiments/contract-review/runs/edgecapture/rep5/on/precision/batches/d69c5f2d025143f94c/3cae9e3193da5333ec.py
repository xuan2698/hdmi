def reference(vectors):
    out = 0
    prev_in = 0
    mask = (1 << 32) - 1
    result = []
    for row in vectors:
        reset = row.get('reset', 0)
        in_val = row.get('in', 0) & mask
        if reset == 1:
            out = 0
            prev_in = in_val
        else:
            transitions = prev_in & ((~in_val) & mask)
            out = (out | transitions) & mask
            prev_in = in_val
        result.append({'out': out})
    return result
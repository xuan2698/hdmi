def reference(vectors):
    mask = (1 << 32) - 1
    out_val = 0
    prev_val = None
    result = []
    for row in vectors:
        in_val = row["in"] & mask
        if row["reset"]:
            out_val = 0
        else:
            if prev_val is not None:
                out_val = out_val | (prev_val & (~in_val) & mask)
        prev_val = in_val
        result.append({"out": out_val})
    return result

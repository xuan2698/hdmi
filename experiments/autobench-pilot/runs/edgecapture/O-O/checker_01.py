def reference(vectors):
    mask = (1 << 32) - 1
    out_val = 0
    out_unknown = mask
    prev_val = 0
    prev_unknown = mask
    result = []
    for row in vectors:
        in_val = row["in"] & mask
        if row["reset"]:
            new_out_val = 0
            new_out_unknown = 0
        else:
            capture_val = prev_val & (~in_val) & mask
            capture_unknown = prev_unknown & (~in_val) & mask
            new_out_val = out_val | capture_val
            new_out_unknown = (~new_out_val) & (out_unknown | capture_unknown) & mask
        prev_val = in_val
        prev_unknown = 0
        out_val = new_out_val
        out_unknown = new_out_unknown
        result.append({"out": None if out_unknown else out_val})
    return result

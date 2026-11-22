def reference(vectors):
    q = 0
    cur_d = 0
    cur_reset = 0
    out = []
    for row in vectors:
        if 'd' in row:
            cur_d = row['d']
        if 'reset' in row:
            cur_reset = row['reset']
        # Rule sync_reset_to_34: reset == 1 at sampled negative edge loads 0x34.
        # Rule load_d_on_negedge_when_not_reset: reset == 0 loads d on negative edge.
        if cur_reset == 1:
            q = 0x34
        else:
            q = cur_d & 0xFF
        out.append({'q': q})
        # Mid input changes occur after sampling, before the other edge,
        # and are carried to the start of the next row.
        if 'mid' in row:
            mid = row['mid']
            if 'd' in mid:
                cur_d = mid['d']
            if 'reset' in mid:
                cur_reset = mid['reset']
    return out

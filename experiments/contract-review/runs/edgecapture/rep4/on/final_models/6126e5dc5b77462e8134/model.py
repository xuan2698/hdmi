def reference(vectors):
    out_reg = 0
    prev_in = 0
    cur_in = 0
    cur_reset = 0
    result = []
    for row in vectors:
        # Apply inputs driven before the sampled posedge
        if 'reset' in row:
            cur_reset = row['reset']
        if 'in' in row:
            cur_in = row['in']
        sampled_reset = cur_reset & 1
        sampled_in = cur_in & 0xFFFFFFFF
        # Rule sync_active_high_reset: synchronous active high reset clears out_reg
        if sampled_reset == 1:
            out_reg = 0
        else:
            # Rule capture_sticky_one_to_zero: capture 1-to-0 transitions per bit
            transition = (~sampled_in) & prev_in & 0xFFFFFFFF
            out_reg = (out_reg | transition) & 0xFFFFFFFF
        # prev_in updates on every posedge, including reset cycles
        prev_in = sampled_in
        result.append({'out': out_reg})
        # Process optional mid-row changes after sampling, before next posedge
        if 'mid' in row:
            mid = row['mid']
            if mid is not None:
                if 'reset' in mid:
                    cur_reset = mid['reset']
                if 'in' in mid:
                    cur_in = mid['in']
    return result
